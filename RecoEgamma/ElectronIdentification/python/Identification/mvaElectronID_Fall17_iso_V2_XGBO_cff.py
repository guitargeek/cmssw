import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import *
from os import path

mvaTag = "Fall17IsoV2XGBO"

weightFileDir = "RecoEgamma/ElectronIdentification/data/XGBOWeightFiles/Fall17IsoV2"

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

mvaEleID_Fall17_iso_V2_XGBO_wpHZZ_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-iso-V2-XGBO-wpHZZ", mvaTag = mvaTag,
    cutCategory0 = "-0.270762339857", # EB1_5
    cutCategory1 = "-0.645976541624", # EB2_5
    cutCategory2 = "-0.962715545197", # EE_5
    cutCategory3 = "2.50067715283", # EB1_10
    cutCategory4 = "2.23564126606", # EB2_10
    cutCategory5 = "1.17516278233", # EE_10
    )

mvaEleID_Fall17_iso_V2_XGBO_wp80_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-iso-V2-XGBO-wp80", mvaTag = mvaTag,
    cutCategory0 = "1.96746353361 - exp(-pt / 3.65096489011) * 8.53542266385", # EB1_5
    cutCategory1 = "1.21724212125 - exp(-pt / 2.06109535495) * 15.4265313755", # EB2_5
    cutCategory2 = "1.13591960553 - exp(-pt / 2.80930191277) * 11.2507069667", # EE_5
    cutCategory3 = "6.85697500415 - exp(-pt / 12.7660844593) * 8.30496707214", # EB1_10
    cutCategory4 = "6.21566416396 - exp(-pt / 13.2844461775) * 7.08957194317", # EB2_10
    cutCategory5 = "5.28042152886 - exp(-pt / 13.9229918617) * 7.0791331503", # EE_10
    )

mvaEleID_Fall17_iso_V2_XGBO_wpLoose_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-iso-V2-XGBO-wpLoose", mvaTag = mvaTag,
    cutCategory0 = "-0.686846547828", # EB1_5
    cutCategory1 = "-0.999983799937", # EB2_5
    cutCategory2 = "-0.82315546692", # EE_5
    cutCategory3 = "0.0410887733267", # EB1_10
    cutCategory4 = "0.0709067235732", # EB2_10
    cutCategory5 = "0.057016260863", # EE_10
    )

mvaEleID_Fall17_iso_V2_XGBO_wp90_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-iso-V2-XGBO-wp90", mvaTag = mvaTag,
    cutCategory0 = "1.25418052055 - exp(-pt / 3.58816319855) * 8.74930663067", # EB1_5
    cutCategory1 = "0.244904329329 - exp(-pt / 1.91572381144) * 18.7172467704", # EB2_5
    cutCategory2 = "-0.154426859149 - exp(-pt / 2.83326512626) * 10.4535039266", # EE_5
    cutCategory3 = "5.72848613406 - exp(-pt / 11.2768373164) * 8.95077607074", # EB1_10
    cutCategory4 = "5.09835198018 - exp(-pt / 11.5115474557) * 8.45617067821", # EB2_10
    cutCategory5 = "4.12353372467 - exp(-pt / 12.2796522542) * 8.57832504129", # EE_10
    )


mvaEleID_Fall17_iso_V2_XGBO_producer_config = cms.PSet(
    mvaName             = cms.string(mvaClassName),
    mvaTag              = cms.string(mvaTag),
    nCategories         = cms.int32(6),
    categoryCuts        = categoryCuts,
    weightFileNames     = mvaWeightFiles,
    variableDefinition  = cms.string(mvaVariablesFile)
    )

mvaEleID_Fall17_iso_V2_XGBO_wpHZZ = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_XGBO_wpHZZ_container )
mvaEleID_Fall17_iso_V2_XGBO_wp80 = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_XGBO_wp80_container )
mvaEleID_Fall17_iso_V2_XGBO_wpLoose = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_XGBO_wpLoose_container )
mvaEleID_Fall17_iso_V2_XGBO_wp90 = configureVIDMVAEleID( mvaEleID_Fall17_iso_V2_XGBO_wp90_container )

mvaEleID_Fall17_iso_V2_XGBO_wpHZZ.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_iso_V2_XGBO_wp80.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_iso_V2_XGBO_wpLoose.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_iso_V2_XGBO_wp90.isPOGApproved = cms.untracked.bool(False)
