import FWCore.ParameterSet.Config as cms

mvaConfigsForEleProducer = cms.VPSet( )

# Import and add all desired MVAs
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_XGBO_cff \
    import mvaEleID_Fall17_noIso_V2_XGBO_producer_config
mvaConfigsForEleProducer.append( mvaEleID_Fall17_noIso_V2_XGBO_producer_config )

from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_XGBO_cff \
    import mvaEleID_Fall17_iso_V2_XGBO_producer_config
mvaConfigsForEleProducer.append( mvaEleID_Fall17_iso_V2_XGBO_producer_config )

electronMVAValueMapProducer = cms.EDProducer('ElectronMVAValueMapProducer',
                                             # The module automatically detects AOD vs miniAOD, so we configure both
                                             #
                                             # AOD case
                                             #
                                             src = cms.InputTag('gedGsfElectrons'),
                                             #
                                             # miniAOD case
                                             #
                                             srcMiniAOD = cms.InputTag('slimmedElectrons',processName=cms.InputTag.skipCurrentProcess()),
                                             #
                                             # MVA configurations
                                             #
                                             mvaConfigurations = mvaConfigsForEleProducer
                                             )
