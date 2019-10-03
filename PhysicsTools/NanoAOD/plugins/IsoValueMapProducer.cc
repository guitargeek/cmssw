// -*- C++ -*-
//
// Package:    PhysicsTools/NanoAOD
// Class:      IsoValueMapProducer
//
/**\class IsoValueMapProducer IsoValueMapProducer.cc PhysicsTools/NanoAOD/plugins/IsoValueMapProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Marco Peruzzi
//         Created:  Mon, 04 Sep 2017 22:43:53 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/isolations.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/IsolatedTrack.h"

//
// class declaration
//

using std::is_same;

namespace {
  template <class T>
  auto makeValueMap(T const& src, std::vector<float> const& values) {
    auto vMap = std::make_unique<edm::ValueMap<float>>();
    edm::ValueMap<float>::Filler filler(*vMap);
    filler.insert(src, values.begin(), values.end());
    filler.fill();

    return vMap;
  }
}  // namespace

template <typename T>
class IsoValueMapProducer : public edm::global::EDProducer<> {
public:
  explicit IsoValueMapProducer(const edm::ParameterSet& cfg)
      : src_(consumes<edm::View<T>>(cfg.getParameter<edm::InputTag>("src"))),
        relative_(cfg.getParameter<bool>("relative")) {
    using std::make_unique;

    if constexpr (is_same<T, pat::Muon>() || is_same<T, pat::Electron>() || is_same<T, pat::IsolatedTrack>()) {
      produces<edm::ValueMap<float>>("miniIsoChg");
      produces<edm::ValueMap<float>>("miniIsoAll");
      ea_miniiso_ = make_unique<EffectiveAreas>((cfg.getParameter<edm::FileInPath>("EAFile_MiniIso")).fullPath());
      rho_miniiso_ = consumes<double>(cfg.getParameter<edm::InputTag>("rho_MiniIso"));
    }
    if constexpr (is_same<T, pat::Electron>()) {
      produces<edm::ValueMap<float>>("PFIsoChg");
      produces<edm::ValueMap<float>>("PFIsoAll");
      produces<edm::ValueMap<float>>("PFIsoLep");
      produces<edm::ValueMap<float>>("PFIsoAll04");
      ea_pfiso_ = make_unique<EffectiveAreas>((cfg.getParameter<edm::FileInPath>("EAFile_PFIso")).fullPath());
      rho_pfiso_ = consumes<double>(cfg.getParameter<edm::InputTag>("rho_PFIso"));
      pfCandidatesToken_ = consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("pfCandidates"));
    } else if constexpr (is_same<T, pat::Photon>()) {
      produces<edm::ValueMap<float>>("PFIsoChg");
      produces<edm::ValueMap<float>>("PFIsoAll");
      ea_pfiso_chg_ = make_unique<EffectiveAreas>((cfg.getParameter<edm::FileInPath>("EAFile_PFIso_Chg")).fullPath());
      ea_pfiso_neu_ = make_unique<EffectiveAreas>((cfg.getParameter<edm::FileInPath>("EAFile_PFIso_Neu")).fullPath());
      ea_pfiso_pho_ = make_unique<EffectiveAreas>((cfg.getParameter<edm::FileInPath>("EAFile_PFIso_Pho")).fullPath());
      rho_pfiso_ = consumes<double>(cfg.getParameter<edm::InputTag>("rho_PFIso"));
    }
  }

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void produce(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

  // ----------member data ---------------------------

  edm::EDGetTokenT<edm::View<T>> src_;
  const bool relative_;
  edm::EDGetTokenT<double> rho_miniiso_;
  edm::EDGetTokenT<double> rho_pfiso_;
  edm::EDGetTokenT<pat::PackedCandidateCollection> pfCandidatesToken_;
  std::unique_ptr<EffectiveAreas> ea_miniiso_;
  std::unique_ptr<EffectiveAreas> ea_pfiso_;
  std::unique_ptr<EffectiveAreas> ea_pfiso_chg_;
  std::unique_ptr<EffectiveAreas> ea_pfiso_neu_;
  std::unique_ptr<EffectiveAreas> ea_pfiso_pho_;

  float getEtaForEA(const T*) const;
  void doMiniIso(edm::Event&) const;
  void doPFIsoEle(edm::Event&) const;
  void doPFIsoPho(edm::Event&) const;
};

template <typename T>
float IsoValueMapProducer<T>::getEtaForEA(const T* obj) const {
  return obj->eta();
}
template <>
float IsoValueMapProducer<pat::Electron>::getEtaForEA(const pat::Electron* el) const {
  return el->superCluster()->eta();
}
template <>
float IsoValueMapProducer<pat::Photon>::getEtaForEA(const pat::Photon* ph) const {
  return ph->superCluster()->eta();
}

template <typename T>
void IsoValueMapProducer<T>::produce(edm::StreamID streamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  if constexpr (is_same<T, pat::Muon>() || is_same<T, pat::Electron>() || is_same<T, pat::IsolatedTrack>()) {
    doMiniIso(iEvent);
  };
  if constexpr (is_same<T, pat::Electron>()) {
    doPFIsoEle(iEvent);
  }
  if constexpr (is_same<T, pat::Photon>()) {
    doPFIsoPho(iEvent);
  }
}

template <typename T>
void IsoValueMapProducer<T>::doMiniIso(edm::Event& iEvent) const {
  auto src = iEvent.getHandle(src_);
  double rho = iEvent.get(rho_miniiso_);

  unsigned int nInput = src->size();

  std::vector<float> miniIsoChg, miniIsoAll;
  miniIsoChg.reserve(nInput);
  miniIsoAll.reserve(nInput);

  for (const auto& obj : *src) {
    auto iso = obj.miniPFIsolation();
    auto chg = iso.chargedHadronIso();
    auto neu = iso.neutralHadronIso();
    auto pho = iso.photonIso();
    auto ea = ea_miniiso_->getEffectiveArea(std::abs(getEtaForEA(&obj)));
    float R = 10.0 / std::min(std::max(obj.pt(), 50.0), 200.0);
    ea *= std::pow(R / 0.3, 2);
    float scale = relative_ ? 1.0 / obj.pt() : 1;
    miniIsoChg.push_back(scale * chg);
    miniIsoAll.push_back(scale * (chg + std::max(0.0, neu + pho - rho * ea)));
  }

  iEvent.put(makeValueMap(src, miniIsoChg), "miniIsoChg");
  iEvent.put(makeValueMap(src, miniIsoAll), "miniIsoAll");
}

template <>
void IsoValueMapProducer<pat::Photon>::doMiniIso(edm::Event& iEvent) const {}

template <typename T>
void IsoValueMapProducer<T>::doPFIsoEle(edm::Event& iEvent) const {}

template <>
void IsoValueMapProducer<pat::Electron>::doPFIsoEle(edm::Event& iEvent) const {
  auto src = iEvent.getHandle(src_);
  double rho = iEvent.get(rho_pfiso_);

  unsigned int nInput = src->size();

  std::vector<float> PFIsoChg, PFIsoAll, PFIsoAll04, PFIsoLep;
  PFIsoChg.reserve(nInput);
  PFIsoAll.reserve(nInput);
  PFIsoLep.reserve(nInput);
  PFIsoAll04.reserve(nInput);

  auto pfLeptonIsolations = computePfLeptonIsolations(*src, iEvent.get(pfCandidatesToken_));

  for (unsigned int i = 0; i < nInput; ++i) {
    auto const& obj = (*src)[i];
    auto iso = obj.pfIsolationVariables();
    auto chg = iso.sumChargedHadronPt;
    auto neu = iso.sumNeutralHadronEt;
    auto pho = iso.sumPhotonEt;
    auto ea = ea_pfiso_->getEffectiveArea(std::abs(getEtaForEA(&obj)));
    float scale = relative_ ? 1.0 / obj.pt() : 1;
    PFIsoChg.push_back(scale * chg);
    PFIsoAll.push_back(scale * (chg + std::max(0.0, neu + pho - rho * ea)));
    PFIsoLep.push_back(scale * pfLeptonIsolations[i]);
    PFIsoAll04.push_back(scale * (obj.chargedHadronIso() +
                                  std::max(0.0, obj.neutralHadronIso() + obj.photonIso() - rho * ea * 16. / 9.)));
  }

  iEvent.put(makeValueMap(src, PFIsoChg), "PFIsoChg");
  iEvent.put(makeValueMap(src, PFIsoAll), "PFIsoAll");
  iEvent.put(makeValueMap(src, PFIsoLep), "PFIsoLep");
  iEvent.put(makeValueMap(src, PFIsoAll04), "PFIsoAll04");
}

template <typename T>
void IsoValueMapProducer<T>::doPFIsoPho(edm::Event& iEvent) const {}

template <>
void IsoValueMapProducer<pat::Photon>::doPFIsoPho(edm::Event& iEvent) const {
  auto src = iEvent.getHandle(src_);
  double rho = iEvent.get(rho_pfiso_);

  unsigned int nInput = src->size();

  std::vector<float> PFIsoChg, PFIsoAll;
  PFIsoChg.reserve(nInput);
  PFIsoAll.reserve(nInput);

  for (const auto& obj : *src) {
    auto chg = obj.chargedHadronIso();
    auto neu = obj.neutralHadronIso();
    auto pho = obj.photonIso();
    auto ea_chg = ea_pfiso_chg_->getEffectiveArea(std::abs(getEtaForEA(&obj)));
    auto ea_neu = ea_pfiso_neu_->getEffectiveArea(std::abs(getEtaForEA(&obj)));
    auto ea_pho = ea_pfiso_pho_->getEffectiveArea(std::abs(getEtaForEA(&obj)));
    float scale = relative_ ? 1.0 / obj.pt() : 1;
    PFIsoChg.push_back(scale * std::max(0.0, chg - rho * ea_chg));
    PFIsoAll.push_back(PFIsoChg.back() +
                       scale * (std::max(0.0, neu - rho * ea_neu) + std::max(0.0, pho - rho * ea_pho)));
  }

  iEvent.put(makeValueMap(src, PFIsoChg), "PFIsoChg");
  iEvent.put(makeValueMap(src, PFIsoAll), "PFIsoAll");
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
template <typename T>
void IsoValueMapProducer<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("input physics object collection");
  desc.add<bool>("relative")->setComment("compute relative isolation instead of absolute one");
  if constexpr (is_same<T, pat::Muon>() || is_same<T, pat::Electron>() || is_same<T, pat::IsolatedTrack>()) {
    desc.add<edm::FileInPath>("EAFile_MiniIso")
        ->setComment("txt file containing effective areas to be used for mini-isolation pileup subtraction");
    desc.add<edm::InputTag>("rho_MiniIso")
        ->setComment("rho to be used for effective-area based mini-isolation pileup subtraction");
  }
  if constexpr (is_same<T, pat::Electron>()) {
    desc.add<edm::FileInPath>("EAFile_PFIso")
        ->setComment(
            "txt file containing effective areas to be used for PF-isolation pileup subtraction for electrons");
    desc.add<edm::InputTag>("rho_PFIso")
        ->setComment("rho to be used for effective-area based PF-isolation pileup subtraction for electrons");
    desc.add<edm::InputTag>("pfCandidates", {"packedPFCandidates"})
        ->setComment("the PF candidate collection to take the leptons for the lepton isolation from");
  }
  if constexpr (is_same<T, pat::Photon>()) {
    desc.add<edm::InputTag>("mapIsoChg")->setComment("input charged PF isolation calculated in VID for photons");
    desc.add<edm::InputTag>("mapIsoNeu")->setComment("input neutral PF isolation calculated in VID for photons");
    desc.add<edm::InputTag>("mapIsoPho")->setComment("input photon PF isolation calculated in VID for photons");
    desc.add<edm::FileInPath>("EAFile_PFIso_Chg")
        ->setComment(
            "txt file containing effective areas to be used for charged PF-isolation pileup subtraction for photons");
    desc.add<edm::FileInPath>("EAFile_PFIso_Neu")
        ->setComment(
            "txt file containing effective areas to be used for neutral PF-isolation pileup subtraction for photons");
    desc.add<edm::FileInPath>("EAFile_PFIso_Pho")
        ->setComment(
            "txt file containing effective areas to be used for photon PF-isolation pileup subtraction for photons");
    desc.add<edm::InputTag>("rho_PFIso")
        ->setComment("rho to be used for effective-area based PF-isolation pileup subtraction for photons");
  }
  std::string modname;
  if constexpr (is_same<T, pat::Muon>())
    modname += "Muon";
  else if constexpr (is_same<T, pat::Electron>())
    modname += "Ele";
  else if constexpr (is_same<T, pat::Photon>())
    modname += "Pho";
  else if constexpr (is_same<T, pat::IsolatedTrack>())
    modname += "IsoTrack";
  modname += "IsoValueMapProducer";
  descriptions.add(modname, desc);
}

typedef IsoValueMapProducer<pat::Muon> MuonIsoValueMapProducer;
typedef IsoValueMapProducer<pat::Electron> EleIsoValueMapProducer;
typedef IsoValueMapProducer<pat::Photon> PhoIsoValueMapProducer;
typedef IsoValueMapProducer<pat::IsolatedTrack> IsoTrackIsoValueMapProducer;

//define this as a plug-in
DEFINE_FWK_MODULE(MuonIsoValueMapProducer);
DEFINE_FWK_MODULE(EleIsoValueMapProducer);
DEFINE_FWK_MODULE(PhoIsoValueMapProducer);
DEFINE_FWK_MODULE(IsoTrackIsoValueMapProducer);
