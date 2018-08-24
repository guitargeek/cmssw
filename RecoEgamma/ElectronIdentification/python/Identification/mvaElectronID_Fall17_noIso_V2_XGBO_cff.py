import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import *
from os import path

mvaTag = "Fall17NoIsoV2XGBO"

weightFileDir = "RecoEgamma/ElectronIdentification/data/XGBOWeightFiles/Fall17NoIsoV2"

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

mvaEleID_Fall17_noIso_V2_XGBO_wp80_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-noIso-V2-XGBO-wp80", mvaTag = mvaTag,
    cutCategory0 = "2.10905986335 - exp(-pt / 4.32860557106) * 8.69059379855", # EB1_5
    cutCategory1 = "1.06469072008 - exp(-pt / 2.57099705718) * 10.2155644024", # EB2_5
    cutCategory2 = "0.661950018143 - exp(-pt / 2.41060570672) * 12.0583320386", # EE_5
    cutCategory3 = "6.54681394881 - exp(-pt / 13.2446706969) * 8.77519134917", # EB1_10
    cutCategory4 = "5.93037774771 - exp(-pt / 13.6603350676) * 7.57290296113", # EB2_10
    cutCategory5 = "5.19242937951 - exp(-pt / 13.1412531565) * 7.75115317641", # EE_10
    )

mvaEleID_Fall17_noIso_V2_XGBO_wpLoose_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-noIso-V2-XGBO-wpLoose", mvaTag = mvaTag,
    cutCategory0 = "-0.672966271488", # EB1_5
    cutCategory1 = "-0.932629551774", # EB2_5
    cutCategory2 = "-0.84492040043", # EE_5
    cutCategory3 = "-0.128407507955", # EB1_10
    cutCategory4 = "-0.155114701109", # EB2_10
    cutCategory5 = "-0.0584081145903", # EE_10
    )

mvaEleID_Fall17_noIso_V2_XGBO_wp90_container = EleMVARaw_WP(
    idName = "mvaEleID-Fall17-noIso-V2-XGBO-wp90", mvaTag = mvaTag,
    cutCategory0 = "1.65887064071 - exp(-pt / 4.61171629179) * 8.4250492518", # EB1_5
    cutCategory1 = "0.0977686490575 - exp(-pt / 2.28643306188) * 12.9967882301", # EB2_5
    cutCategory2 = "-0.423214949836 - exp(-pt / 2.81611996) * 9.18542520671", # EE_5
    cutCategory3 = "5.44184594082 - exp(-pt / 11.7446323105) * 9.23546261507", # EB1_10
    cutCategory4 = "4.83236756976 - exp(-pt / 11.8509672581) * 8.96137241564", # EB2_10
    cutCategory5 = "4.04999609376 - exp(-pt / 11.5551878137) * 9.52358347156", # EE_10
    )


mvaEleID_Fall17_noIso_V2_XGBO_producer_config = cms.PSet(
    mvaName             = cms.string(mvaClassName),
    mvaTag              = cms.string(mvaTag),
    nCategories         = cms.int32(6),
    categoryCuts        = categoryCuts,
    weightFileNames     = mvaWeightFiles,
    variableDefinition  = cms.string(mvaVariablesFile)
    )

mvaEleID_Fall17_noIso_V2_XGBO_wp80 = configureVIDMVAEleID( mvaEleID_Fall17_noIso_V2_XGBO_wp80_container )
mvaEleID_Fall17_noIso_V2_XGBO_wpLoose = configureVIDMVAEleID( mvaEleID_Fall17_noIso_V2_XGBO_wpLoose_container )
mvaEleID_Fall17_noIso_V2_XGBO_wp90 = configureVIDMVAEleID( mvaEleID_Fall17_noIso_V2_XGBO_wp90_container )

mvaEleID_Fall17_noIso_V2_XGBO_wp80.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_noIso_V2_XGBO_wpLoose.isPOGApproved = cms.untracked.bool(False)
mvaEleID_Fall17_noIso_V2_XGBO_wp90.isPOGApproved = cms.untracked.bool(False)
