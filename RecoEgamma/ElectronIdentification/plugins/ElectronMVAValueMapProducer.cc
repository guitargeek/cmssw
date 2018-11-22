#include "RecoEgamma/EgammaTools/interface/MVAValueMapProducer.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"

// Some specialization of template classes needed for the MVA

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

typedef MVAValueMapProducer<reco::GsfElectron> ElectronMVAValueMapProducer;

//define this as a plug-in
DEFINE_FWK_MODULE(ElectronMVAValueMapProducer);
