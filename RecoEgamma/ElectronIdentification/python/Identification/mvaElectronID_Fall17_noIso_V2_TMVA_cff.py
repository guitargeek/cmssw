import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import *
from os import path

mvaTag = "Fall17NoIsoV2TMVA"

weightFileDir = "RecoEgamma/ElectronIdentification/data/TMVAWeightFiles/Fall17NoIsoV2"

mvaWeightFiles = cms.vstring(
     path.join(weightFileDir, "EB1_5.weights.xml.gz"), # EB1_5
     path.join(weightFileDir, "EB2_5.weights.xml.gz"), # EB2_5
     path.join(weightFileDir, "EE_5.weights.xml.gz"), # EE_5
     path.join(weightFileDir, "EB1_10.weights.xml.gz"), # EB1_10
     path.join(weightFileDir, "EB2_10.weights.xml.gz"), # EB2_10
     path.join(weightFileDir, "EE_10.weights.xml.gz"), # EE_10
     )

categoryCuts = cms.vstring(
     "pt < 10. & abs(superCluster.eta) < 0.800", # EB1_5
     "pt < 10. & abs(superCluster.eta) >= 0.800 & abs(superCluster.eta) < 1.479", # EB2_5
     "pt < 10. & abs(superCluster.eta) >= 1.479", # EE_5
     "pt >= 10. & abs(superCluster.eta) < 0.800", # EB1_10
     "pt >= 10. & abs(superCluster.eta) >= 0.800 & abs(superCluster.eta) < 1.479", # EB2_10
     "pt >= 10. & abs(superCluster.eta) >= 1.479", # EE_10
     )

mvaEleID_Fall17_noIso_V2_TMVA_wp80_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-noIso-V2-TMVA-wp80", mvaTag = mvaTag,
    cutCategory0 = "0.916520954233 - exp(-pt / 1.7895922774) * 4.35884750642", # EB1_5
    cutCategory1 = "0.901454824767 - exp(-pt / 1.43977293111) * 5.3051331295", # EB2_5
    cutCategory2 = "0.908062489462 - exp(-pt / 1.43409501729) * 4.22431334642", # EE_5
    cutCategory3 = "0.981301842001 - exp(-pt / 6.27744992903) * 4.09138944271", # EB1_10
    cutCategory4 = "0.967764100944 - exp(-pt / 7.06318879051) * 3.61146027444", # EB2_10
    cutCategory5 = "0.957859095169 - exp(-pt / 9.12017640324) * 3.2131291261", # EE_10
    )

mvaEleID_Fall17_noIso_V2_TMVA_wpLoose_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-noIso-V2-TMVA-wpLoose", mvaTag = mvaTag,
    cutCategory0 = "0.494218351002", # EB1_5
    cutCategory1 = "0.463958900264", # EB2_5
    cutCategory2 = "0.670124009185", # EE_5
    cutCategory3 = "-0.871636482584", # EB1_10
    cutCategory4 = "-0.829357525261", # EB2_10
    cutCategory5 = "-0.754091261262", # EE_10
    )

mvaEleID_Fall17_noIso_V2_TMVA_wp90_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-noIso-V2-TMVA-wp90", mvaTag = mvaTag,
    cutCategory0 = "0.852544796124 - exp(-pt / 1.98183992256) * 5.72943551324", # EB1_5
    cutCategory1 = "0.742733312033 - exp(-pt / 1.41426000038) * 11.0075075281", # EB2_5
    cutCategory2 = "0.649589039355 - exp(-pt / 1.56828093085) * 7.42152086653", # EE_5
    cutCategory3 = "0.962801552475 - exp(-pt / 8.01473751866) * 5.02278204414", # EB1_10
    cutCategory4 = "0.92166798972 - exp(-pt / 9.3018873342) * 4.47027589629", # EB2_10
    cutCategory5 = "0.887007919245 - exp(-pt / 12.2733688693) * 3.85062088681", # EE_10
    )


mvaEleID_Fall17_noIso_V2_TMVA_producer_config = cms.PSet(
    mvaName             = cms.string(mvaClassName),
    mvaTag              = cms.string(mvaTag),
    nCategories         = cms.int32(6),
    categoryCuts        = categoryCuts,
    weightFileNames     = mvaWeightFiles,
    variableDefinition  = cms.string(mvaVariablesFile)
    )

mvaEleID_Fall17_noIso_V2_TMVA_wp80 = configureVIDMVAEleID( mvaEleID_Fall17_noIso_V2_TMVA_wp80_container )
mvaEleID_Fall17_noIso_V2_TMVA_wpLoose = configureVIDMVAEleID( mvaEleID_Fall17_noIso_V2_TMVA_wpLoose_container )
mvaEleID_Fall17_noIso_V2_TMVA_wp90 = configureVIDMVAEleID( mvaEleID_Fall17_noIso_V2_TMVA_wp90_container )

mvaEleID_Fall17_noIso_V2_TMVA_wp80.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_noIso_V2_TMVA_wpLoose.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_noIso_V2_TMVA_wp90.isPOGApproved = cms.untracked.bool(False)
