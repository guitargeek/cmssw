#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <optional>
#include <iostream>
#include <tinyxml2.h>

namespace {

  // join vector of strings to one string
  std::string join(const std::vector<std::string>& vec, const char* delim) {
    std::stringstream res;
    std::copy(vec.begin(), vec.end(), std::ostream_iterator<std::string>(res, delim));
    return res.str();
  }

  struct LHEWeightInfo {
    std::string id;
    std::string text;
    std::optional<std::string> group = std::nullopt;
  };

  void foo(tinyxml2::XMLElement* root, int level, std::optional<std::string> group, std::vector<LHEWeightInfo> & out) {
     for (auto* elem = root->FirstChildElement(); elem != nullptr;
          elem = elem->NextSiblingElement()) {
       if (strcmp(elem->Name(), "weight") == 0) {
         std::string text = "";
         if (elem->GetText())
           text = elem->GetText();
         out.push_back({elem->Attribute("id"), text, group});
       } else if (strcmp(elem->Name(), "weightgroup") == 0) {
          if(level == 0) {
            foo(elem, level  + 1, elem->Attribute("name"), out);
          } else if(level == 1) {

            // We end up here if we find a weightgroup in a weightgroup.
            // This happens at least from Madgraph 2.6.5 on, because two lines in the LHE header are
            // flipped by mistake (see line 3 and 4 below). That makes the XML inconsistent.
            // The work around here is instead of trying to descend into this nested weight group,
            // we just update the name of the loop and continue in the current group.
            //
            //  1 <weightgroup name="NNPDF31_nnlo_as_0118_mc_hessian_pdfas" combine="symmhessian+as">
            //  2 <weight id="1001" MUR="1.0" MUF="1.0" PDF="325300" >  </weight>
            //  3 <weightgroup name="Central scale variation" combine="envelope">
            //  4 </weightgroup> PDF
            //  5 <weight id="1002" MUR="1.0" MUF="1.0" DYN_SCALE="1" PDF="325300" > dyn_scale_choice=sum pt  </weight>
            //  6 <weight id="1003" MUR="1.0" MUF="1.0" DYN_SCALE="2" PDF="325300" > dyn_scale_choice=HT  </weight>
            //  7 <weight id="1004" MUR="1.0" MUF="1.0" DYN_SCALE="3" PDF="325300" > dyn_scale_choice=HT/2  </weight>
            //  8 <weight id="1005" MUR="1.0" MUF="1.0" DYN_SCALE="4" PDF="325300" > dyn_scale_choice=sqrts  </weight>
            //  9 <weight id="1006" MUR="2.0" MUF="1.0" PDF="325300" > MUR=2.0  </weight>
            //   ...
            // 10 </weightgroup> # scale

            group = elem->Attribute("name");
          } else {
            throw cms::Exception("LogicError", "Somethings is really wrong in the initrwgt header\n");
          }
        }
     }
  }

  std::vector<LHEWeightInfo> getLHEWeightInfos(LHERunInfoProduct const& lheInfo) {
    std::vector<LHEWeightInfo> out;

    for (auto iter = lheInfo.headers_begin(), end = lheInfo.headers_end(); iter != end; ++iter) {
      if (iter->tag() != "initrwgt") {
        continue;
      }

      tinyxml2::XMLDocument xmlDoc;
      xmlDoc.Parse(("<root>" + join(iter->lines(), "") + "</root>").c_str());
      tinyxml2::XMLElement* root = xmlDoc.FirstChildElement("root");

      foo(root, 0, std::nullopt, out);
    }

    return out;
  }

}  // namespace

class LHEWeightsTableProducer : public edm::global::EDProducer<edm::RunCache<std::vector<LHEWeightInfo>>> {
public:
  LHEWeightsTableProducer(edm::ParameterSet const& params)
      : lheInputTag_(params.getParameter<edm::InputTag>("lheInfo")),
        lheToken_(consumes<LHEEventProduct>(params.getParameter<edm::InputTag>("lheInfo"))),
        weightgroups_(params.getParameter<std::vector<std::string>>("weightgroups")),
        lheWeightPrecision_(params.getParameter<int32_t>("lheWeightPrecision")) {
    consumes<LHERunInfoProduct, edm::InRun>(lheInputTag_);
    produces<std::vector<nanoaod::FlatTable>>();
  }

  void produce(edm::StreamID id, edm::Event& iEvent, const edm::EventSetup& iSetup) const override {
    // tables for LHE weights, may not be filled
    edm::Handle<LHEEventProduct> lheHandle;
    iEvent.getByToken(lheToken_, lheHandle);
    auto const& lheInfo = *lheHandle;

    auto lheWeightTables = std::make_unique<std::vector<nanoaod::FlatTable>>();
    auto const& weightInfos = *runCache(iEvent.getRun().index());

    double w0 = lheInfo.originalXWGTUP();

    int i = 0;
    if (lheInfo.weights().size() != weightInfos.size()) {
      throw cms::Exception("LogicError", "Weight labels don't have the same size as weights!\n");
    }
    std::unordered_map<std::string, std::pair<std::string, std::vector<float>>> groupsWithWeights;
    for (auto const& weight : lheInfo.weights()) {
      auto& val = weightInfos[i].group ? groupsWithWeights[*weightInfos[i].group] : groupsWithWeights["ungrouped"];
      if (val.first.empty()) {
        val.first += ";id,text";
      }
      val.first += ";" + weightInfos[i].id + "," + weightInfos[i].text;
      val.second.push_back(weight.wgt / w0);
      ++i;
    }
    for (auto const& group : groupsWithWeights) {
      if (std::find(weightgroups_.begin(), weightgroups_.end(), group.first) == weightgroups_.end()) {
        continue;
      }
      std::string name = std::string("LHEWeight_") + group.first;
      std::transform(name.begin(), name.end(), name.begin(), [](char ch) { return ch == ' ' ? '_' : ch; });
      std::string doc = group.first + " (w_var / w_nominal)" + group.second.first;
      lheWeightTables->emplace_back(group.second.second.size(), name, false);
      lheWeightTables->back().addColumn<float>(
          "", group.second.second, doc, nanoaod::FlatTable::FloatColumn, lheWeightPrecision_);
    }

    iEvent.put(std::move(lheWeightTables));
  }

  std::shared_ptr<std::vector<LHEWeightInfo>> globalBeginRun(edm::Run const& iRun,
                                                             edm::EventSetup const&) const override {
    edm::Handle<LHERunInfoProduct> lheInfo;

    auto weightChoice = std::make_shared<std::vector<LHEWeightInfo>>();

    // getByToken throws since we're not in the endRun (see https://github.com/cms-sw/cmssw/pull/18499)
    iRun.getByLabel(lheInputTag_, lheInfo);
    if (lheInfo.isValid()) {
      getLHEWeightInfos(*lheInfo).swap(*weightChoice);
    }

    return weightChoice;
  }

  // nothing to do here
  void globalEndRun(edm::Run const&, edm::EventSetup const&) const override {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    edm::ParameterSetDescription desc;
    desc.add<edm::InputTag>("lheInfo", {"externalLHEProducer"})
        ->setComment("tag(s) for the LHE information (LHEEventProduct and LHERunInfoProduct)");
    desc.add<std::vector<std::string>>("weightgroups");
    desc.add<int32_t>("lheWeightPrecision", -1)->setComment("Number of bits in the mantissa for LHE weights");
    descriptions.addDefault(desc);
  }

protected:
  const edm::InputTag lheInputTag_;
  const edm::EDGetTokenT<LHEEventProduct> lheToken_;
  const std::vector<std::string> weightgroups_;
  int lheWeightPrecision_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(LHEWeightsTableProducer);
