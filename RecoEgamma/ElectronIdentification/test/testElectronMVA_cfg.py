import FWCore.ParameterSet.Config as cms
# from RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi import electronMVAVariableHelper
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
from Configuration.AlCa.GlobalTag import GlobalTag

process = cms.Process("ElectronMVANtuplizer")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# File with the ID variables to include in the Ntuplizer
mvaVariablesFile = "RecoEgamma/ElectronIdentification/data/ElectronIDVariables.txt"

outputFile = "electron_validation_ntuple.root"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
         '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/RECOSIMstep_94X_mc2017_realistic_v10-v1/00000/0293A280-B5F3-E711-8303-3417EBE33927.root'
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
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_XGBO_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_XGBO_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_TMVA_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_TMVA_cff',
                 ]

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

process.ntuplizer = cms.EDAnalyzer('ElectronMVANtuplizer',
        # AOD case
        src                  = cms.InputTag('gedGsfElectrons'),
        vertices             = cms.InputTag('offlinePrimaryVertices'),
        pileup               = cms.InputTag('addPileupInfo'),
        genParticles         = cms.InputTag('genParticles'),
        # miniAOD case
        srcMiniAOD           = cms.InputTag('slimmedElectrons'),
        verticesMiniAOD      = cms.InputTag('offlineSlimmedPrimaryVertices'),
        pileupMiniAOD        = cms.InputTag('slimmedAddPileupInfo'),
        genParticlesMiniAOD  = cms.InputTag('prunedGenParticles'),
        #
        eleMVAs             = cms.untracked.vstring(
                                          ),
        eleMVALabels        = cms.untracked.vstring(
                                          ),
        eleMVAValMaps        = cms.untracked.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2XGBOValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2XGBORawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2XGBOValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2XGBORawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2TMVAValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2TMVARawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2TMVAValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2TMVARawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1RawValues",
                                           ),
        eleMVAValMapLabels   = cms.untracked.vstring(
                                           "Spring16GPVals",
                                           "Spring16GPRawVals",
                                           "Spring16HZZVals",
                                           "Spring16HZZRawVals",
                                           "Fall17NoIsoV2XGBOVals",
                                           "Fall17NoIsoV2XGBORawVals",
                                           "Fall17IsoV2XGBOVals",
                                           "Fall17IsoV2XGBORawVals",
                                           "Fall17NoIsoV2TMVAVals",
                                           "Fall17NoIsoV2TMVARawVals",
                                           "Fall17IsoV2TMVAVals",
                                           "Fall17IsoV2TMVARawVals",
                                           "Fall17NoIsoV2Vals",
                                           "Fall17NoIsoV2RawVals",
                                           "Fall17IsoV2Vals",
                                           "Fall17IsoV2RawVals",
                                           "Fall17IsoV1Vals",
                                           "Fall17IsoV1RawVals",
                                           "Fall17NoIsoV1Vals",
                                           "Fall17NoIsoV1RawVals",
                                           ),
        eleMVACats           = cms.untracked.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Categories",
                                           ),
        eleMVACatLabels      = cms.untracked.vstring(
                                           "EleMVACats",
                                           ),
        #
        variableDefinition   = cms.string(mvaVariablesFile),
        isMC                 = cms.bool(True),
        deltaR               = cms.double(0.1),
        )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( outputFile )
                                   )

process.p = cms.Path(process.egmGsfElectronIDSequence * process.ntuplizer)
