import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
from Configuration.AlCa.GlobalTag import GlobalTag

process = cms.Process("ElectronMVANtuplizer")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# File with the ID variables to include in the Ntuplizer
mvaVariablesFile = "RecoEgamma/ElectronIdentification/data/ElectronIDVariables.txt"

outputFile = "electron_ntuple.root"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

# I want to use the following sample for the paper:
# /DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM
# I found this with dasgoclient -query="dataset=/DYJetsToLL_M-50_TuneCP5*/*2017*/MINIAODSIM"

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/A8FE9F01-CC47-E811-B7EC-801844DEE7F8.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/D06201D7-1649-E811-A05B-782BCB20EDFD.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/0CB519C6-7649-E811-98DA-001C23C0B671.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/26E635BA-A249-E811-80BF-F01FAFE5F3BD.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/AA36A86B-334D-E811-BFE3-44A842CFD60C.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/8E327574-6E4D-E811-AA66-001CC4A6FBE0.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/C2538B0F-2554-E811-B6AB-0242AC130002.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/4C5B133D-B455-E811-B0F6-24BE05CECBD1.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/36EFF00B-C155-E811-9B17-E0071B7A4550.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/AE91AC98-DB55-E811-B46C-EC0D9A82264E.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/12E309BB-F655-E811-8EF4-EC0D9A8221CE.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/F0A580EB-EE56-E811-A68F-F01FAFE5CF52.root',
        '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_94X_mc2017_realistic_v11-v1/70000/A42889A7-5856-E811-96C2-A4BF0102611B.root',
    )
)

useAOD = False

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate
if useAOD == True :
    dataFormat = DataFormat.AOD
else :
    dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_XGBO_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_XGBO_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_TMVA_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_TMVA_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_HZZ_cff',
                 ]

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

process.ntuplizer = cms.EDAnalyzer('ElectronMVANtuplizer',
        #
        eleMVAs             = cms.untracked.vstring(
                                          "egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Spring16-HZZ-V1-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-HZZ-wpHZZ",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wpHZZ",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-XGBO-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-XGBO-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-XGBO-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-XGBO-wpHZZ",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-XGBO-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-XGBO-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-XGBO-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-TMVA-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-TMVA-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-TMVA-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-TMVA-wpHZZ",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-TMVA-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-TMVA-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-TMVA-wp90",
                                          ),
        eleMVALabels        = cms.untracked.vstring(
                                          "Spring16GPV1wp80",
                                          "Spring16GPV1wp90",
                                          "Spring16HZZV1wpLoose",
                                          "Fall17noIsoV1wp90",
                                          "Fall17noIsoV1wp80",
                                          "Fall17noIsoV1wpLoose",
                                          "Fall17isoV1wp90",
                                          "Fall17isoV1wp80",
                                          "Fall17isoV1wpLoose",
                                          "Fall17isoV2HZZwpHZZ",
                                          "Fall17noIsoV2wp80",
                                          "Fall17noIsoV2wpLoose",
                                          "Fall17noIsoV2wp90",
                                          "Fall17isoV2wpHZZ",
                                          "Fall17isoV2wp80",
                                          "Fall17isoV2wpLoose",
                                          "Fall17isoV2wp90",
                                          "Fall17noIsoV2XGBOwp80",
                                          "Fall17noIsoV2XGBOwpLoose",
                                          "Fall17noIsoV2XGBOwp90",
                                          "Fall17isoV2XGBOwpHZZ",
                                          "Fall17isoV2XGBOwp80",
                                          "Fall17isoV2XGBOwpLoose",
                                          "Fall17isoV2XGBOwp90",
                                          "Fall17noIsoV2TMVAwp80",
                                          "Fall17noIsoV2TMVAwpLoose",
                                          "Fall17noIsoV2TMVAwp90",
                                          "Fall17isoV2TMVAwpHZZ",
                                          "Fall17isoV2TMVAwp80",
                                          "Fall17isoV2TMVAwpLoose",
                                          "Fall17isoV2TMVAwp90",
                                          ),
        eleMVAValMaps        = cms.untracked.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2HZZRawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2XGBORawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2XGBORawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2TMVARawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2TMVARawValues",
                                           ),
        eleMVAValMapLabels   = cms.untracked.vstring(
                                           "Spring16GPV1Vals",
                                           "Spring16HZZV1Vals",
                                           "Fall17IsoV1Vals",
                                           "Fall17NoIsoV1Vals",
                                           "Fall17IsoV2HZZVals",
                                           "Fall17IsoV2Vals",
                                           "Fall17NoIsoV2Vals",
                                           "Fall17IsoV2XGBOVals",
                                           "Fall17NoIsoV2XGBOVals",
                                           "Fall17IsoV2TMVAVals",
                                           "Fall17NoIsoV2TMVAVals",
                                           ),
        eleMVACats           = cms.untracked.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Categories",
                                           ),
        eleMVACatLabels      = cms.untracked.vstring(
                                           "EleMVACats",
                                           ),
        #
        variableDefinition   = cms.string(mvaVariablesFile),
        ptThreshold = cms.double(5.0),
        )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( outputFile )
                                   )

process.p = cms.Path(process.egmGsfElectronIDSequence * process.ntuplizer)
