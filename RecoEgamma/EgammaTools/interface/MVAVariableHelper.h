#ifndef RecoEgamma_EgammaTools_MVAVariableHelper_H
#define RecoEgamma_EgammaTools_MVAVariableHelper_H

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "FWCore/Framework/interface/Event.h"

#include <unordered_map>
#include <vector>
#include <string>

template<class ParticleType>
class MVAVariableIndexMap {

  public:

    MVAVariableIndexMap() : indexMap_({}) {}

    int getIndex(std::string const& name) const { return indexMap_.at(name); }

  private:

    const std::unordered_map<std::string, int> indexMap_;
};

template<class ParticleType>
class MVAVariableHelper {

  public:

    MVAVariableHelper(edm::ConsumesCollector && cc)
        : tokens_({})
    {}

    const std::vector<float> getAuxVariables(edm::Ptr<ParticleType> const& particlePtr,
                                             const edm::Event& iEvent) const
    { return std::vector<float>{}; }

  private:

    const std::vector<edm::EDGetToken> tokens_;
};

namespace {

    float getVariableFromValueMapToken(edm::Ptr<reco::GsfElectron> const& particlePtr,
                                       edm::EDGetToken const& token, edm::Event const& iEvent) {
        edm::Handle<edm::ValueMap<float>> handle;
        iEvent.getByToken(token, handle);
        return (*handle)[particlePtr];
    }

    float getVariableFromDoubleToken(edm::EDGetToken const& token, const edm::Event& iEvent) {
        edm::Handle<double> handle;
        iEvent.getByToken(token, handle);
        return *handle;
    }
};

////
// For the electrons
////

template<>
MVAVariableHelper<reco::GsfElectron>::MVAVariableHelper(edm::ConsumesCollector && cc)
    : tokens_({
            cc.consumes<edm::ValueMap<float>>(edm::InputTag("electronMVAVariableHelper", "kfhits")),
            cc.consumes<edm::ValueMap<float>>(edm::InputTag("electronMVAVariableHelper", "kfchi2")),
            cc.consumes<edm::ValueMap<float>>(edm::InputTag("electronMVAVariableHelper", "convVtxFitProb")),
            cc.consumes<double>(edm::InputTag("fixedGridRhoFastjetAll"))
        })
{}

template<>
MVAVariableIndexMap<reco::GsfElectron>::MVAVariableIndexMap()
    : indexMap_({
            {"electronMVAVariableHelper:kfhits"        , 0},
            {"electronMVAVariableHelper:kfchi2"        , 1},
            {"electronMVAVariableHelper:convVtxFitProb", 2},
            {"fixedGridRhoFastjetAll"                  , 3}
        })
{}

template<>
const std::vector<float> MVAVariableHelper<reco::GsfElectron>::getAuxVariables(
        edm::Ptr<reco::GsfElectron> const& particlePtr, const edm::Event& iEvent) const
{
    return std::vector<float> {
        getVariableFromValueMapToken(particlePtr, tokens_[0], iEvent),
        getVariableFromValueMapToken(particlePtr, tokens_[1], iEvent),
        getVariableFromValueMapToken(particlePtr, tokens_[2], iEvent),
        getVariableFromDoubleToken(tokens_[3], iEvent)
    };
}

#endif
