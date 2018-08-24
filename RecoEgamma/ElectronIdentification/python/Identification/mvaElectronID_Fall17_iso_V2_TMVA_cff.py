import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import *
from os import path

mvaTag = "Fall17IsoV2TMVA"

weightFileDir = "RecoEgamma/ElectronIdentification/data/TMVAWeightFiles/Fall17IsoV2"

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

mvaEleID_Fall17_iso_V2_TMVA_wpHZZ_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-iso-V2-TMVA-wpHZZ", mvaTag = mvaTag,
    cutCategory0 = "0.618335256647", # EB1_5
    cutCategory1 = "0.606342578661", # EB2_5
    cutCategory2 = "0.649842200964", # EE_5
    cutCategory3 = "-0.0392662617146", # EB1_10
    cutCategory4 = "-0.0320653784951", # EB2_10
    cutCategory5 = "-0.374749012691", # EE_10
    )

mvaEleID_Fall17_iso_V2_TMVA_wp80_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-iso-V2-TMVA-wp80", mvaTag = mvaTag,
    cutCategory0 = "0.941141141375 - exp(-pt / 1.78651170653) * 3.49997609798", # EB1_5
    cutCategory1 = "0.924761436733 - exp(-pt / 1.24221089353) * 7.03525453405", # EB2_5
    cutCategory2 = "0.918964717155 - exp(-pt / 1.38374115548) * 3.80969252867", # EE_5
    cutCategory3 = "0.986152636103 - exp(-pt / 6.15866701211) * 2.56567962552", # EB1_10
    cutCategory4 = "0.972608145298 - exp(-pt / 6.89149836744) * 2.34293540575", # EB2_10
    cutCategory5 = "0.963599605507 - exp(-pt / 9.26359242856) * 2.65755100468", # EE_10
    )

mvaEleID_Fall17_iso_V2_TMVA_wpLoose_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-iso-V2-TMVA-wpLoose", mvaTag = mvaTag,
    cutCategory0 = "0.477545400166", # EB1_5
    cutCategory1 = "0.417807802735", # EB2_5
    cutCategory2 = "0.638998026394", # EE_5
    cutCategory3 = "-0.848914950589", # EB1_10
    cutCategory4 = "-0.791676645382", # EB2_10
    cutCategory5 = "-0.734591691193", # EE_10
    )

mvaEleID_Fall17_iso_V2_TMVA_wp90_container = EleMVA_WP(
    idName = "mvaEleID-Fall17-iso-V2-TMVA-wp90", mvaTag = mvaTag,
    cutCategory0 = "0.892129328963 - exp(-pt / 1.96225302923) * 4.91656117952", # EB1_5
    cutCategory1 = "0.809094744549 - exp(-pt / 1.25431266984) * 14.6810051803", # EB2_5
    cutCategory2 = "0.711281146429 - exp(-pt / 1.39557843505) * 9.88824807742", # EE_5
    cutCategory3 = "0.965562334706 - exp(-pt / 7.22482287391) * 4.49723680929", # EB1_10
    cutCategory4 = "0.922153254232 - exp(-pt / 8.21891171804) * 4.14585333726", # EB2_10
    cutCategory5 = "0.898195725163 - exp(-pt / 12.0147915574) * 3.6896602709", # EE_10
    )


mvaEleID_Fall17_iso_V2_TMVA_producer_config = cms.PSet(
    mvaName             = cms.string(mvaClassName),
    mvaTag              = cms.string(mvaTag),
    nCategories         = cms.int32(6),
    categoryCuts        = categoryCuts,
    weightFileNames     = mvaWeightFiles,
    variableDefinition  = cms.string(mvaVariablesFile)
    )

mvaEleID_Fall17_iso_V2_TMVA_wpHZZ = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_TMVA_wpHZZ_container )
mvaEleID_Fall17_iso_V2_TMVA_wp80 = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_TMVA_wp80_container )
mvaEleID_Fall17_iso_V2_TMVA_wpLoose = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_TMVA_wpLoose_container )
mvaEleID_Fall17_iso_V2_TMVA_wp90 = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_TMVA_wp90_container )

mvaEleID_Fall17_iso_V2_TMVA_wpHZZ.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_iso_V2_TMVA_wp80.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_iso_V2_TMVA_wpLoose.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_iso_V2_TMVA_wp90.isPOGApproved = cms.untracked.bool(False)
