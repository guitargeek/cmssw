import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import *
from os import path

mvaTag = "Fall17IsoV2HZZ"

weightFileDir = "RecoEgamma/ElectronIdentification/data/MVAWeightFiles/Fall17IsoV2HZZ"

mvaWeightFiles = cms.vstring(
     path.join(weightFileDir, "EB1_5.weights.xml.gz"), # EB1_5
     path.join(weightFileDir, "EB2_5.weights.xml.gz"), # EB2_5
     path.join(weightFileDir, "EE_5.weights.xml.gz"), # EE_5
     path.join(weightFileDir, "EB1_10.weights.xml.gz"), # EB1_10
     path.join(weightFileDir, "EB2_10.weights.xml.gz"), # EB2_10
     path.join(weightFileDir, "EE_10.weights.xml.gz"), # EE_10
     )

categoryCuts = cms.vstring(
     "pt < 10. && abs(superCluster.eta) < 0.800", # EB1_5
     "pt < 10. && abs(superCluster.eta) >= 0.800 && abs(superCluster.eta) < 1.479", # EB2_5
     "pt < 10. && abs(superCluster.eta) >= 1.479", # EE_5
     "pt >= 10. && abs(superCluster.eta) < 0.800", # EB1_10
     "pt >= 10. && abs(superCluster.eta) >= 0.800 && abs(superCluster.eta) < 1.479", # EB2_10
     "pt >= 10. && abs(superCluster.eta) >= 1.479", # EE_10
     )

mvaEleID_Fall17_iso_V2_HZZ_wpHZZ_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-iso-V2-HZZ-wpHZZ", mvaTag = mvaTag,
    cutCategory0 = "0.6282314508618512", # EB1_5
    cutCategory1 = "0.5922759800216235", # EB2_5
    cutCategory2 = "0.636928856343224", # EE_5
    cutCategory3 = "0.03554496382023676", # EB1_10
    cutCategory4 = "0.04342450751424789", # EB2_10
    cutCategory5 = "-0.266000023716261", # EE_10
    )

mvaEleID_Fall17_iso_V2_HZZ_producer_config = cms.PSet(
    mvaName             = cms.string(mvaClassName),
    mvaTag              = cms.string(mvaTag),
    nCategories         = cms.int32(6),
    categoryCuts        = categoryCuts,
    weightFileNames     = mvaWeightFiles,
    variableDefinition  = cms.string(mvaVariablesFile)
    )

mvaEleID_Fall17_iso_V2_HZZ_wpHZZ = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_HZZ_wpHZZ_container )

mvaEleID_Fall17_iso_V2_HZZ_wpHZZ.isPOGApproved = cms.untracked.bool(True)
