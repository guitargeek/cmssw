# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --filein dbs:/ZZTo4L_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM --fileout file:HIG-RunIISummer16NanoAODv4-00121.root --mc --eventcontent NANOEDMAODSIM --datatier NANOAODSIM --processName 14Dec2018 --conditions 102X_mcRun2_asymptotic_v6 --customise_commands process.particleLevelSequence.remove(process.genParticles2HepMCHiggsVtx);process.particleLevelSequence.remove(process.rivetProducerHTXS);process.particleLevelTables.remove(process.HTXSCategoryTable) --step NANO --nThreads 2 --era Run2_2016,run2_nanoAOD_94X2016 --python_filename HIG-RunIISummer16NanoAODv4-00121_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 5236
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('14Dec2018',eras.Run2_2016,eras.run2_nanoAOD_94X2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/983AB234-DBC6-E811-9362-001A649D4D09.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/42BA2638-E9C6-E811-9BEB-001A649D47FD.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/CE9F3874-CFC6-E811-817D-001A649D45CD.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/96C16C4E-D2C6-E811-9013-001A647A9326.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/F48FA5AA-CFC6-E811-A71A-001A649D4905.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/206968F5-D0C6-E811-8341-001A649D4DF1.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/C68381F3-D0C6-E811-9CD7-001A649D4E75.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/28324326-D1C6-E811-99BD-001A649D4F95.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/6250ECF5-D2C6-E811-99B2-001A647A95F6.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/7ED00003-D4C6-E811-82E0-001A649D4FBD.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/8C99EED6-DBC6-E811-9905-001A6499E6AC.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/9845F723-D8C6-E811-B1A4-001A647A944E.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/8462D5B0-DCC6-E811-96EC-001A647A947A.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/1C690301-D9C6-E811-A42A-480FCFF4FC90.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/56A45EDD-DBC6-E811-8514-001A649D4E65.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/82682EA4-DCC6-E811-938C-001A649D475D.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/C49B4DD0-DFC6-E811-9B51-001A647A9202.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/A4E5EEDB-DBC6-E811-AE9C-00215E702674.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/8CF83018-E5C6-E811-94B5-00215E3F8CDC.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/DC9147BD-E5C6-E811-9048-001A649D1E05.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/DEB1FA30-E3C6-E811-B591-001A649D4989.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/F01E86DA-E8C6-E811-94D9-001A647A945A.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/E4A25CEB-E3C6-E811-80B6-001A649D471D.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/6A984068-E4C6-E811-9DEC-001A647A9362.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/EE55A1D4-E9C6-E811-AAAF-001A649D4AED.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/6AC5E249-E8C6-E811-851D-001A649D4D95.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/386C8F67-EFC6-E811-AE2E-001A649D45CD.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/5C7892CC-E8C6-E811-BD41-001A649D5019.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/C46E7E5C-EBC6-E811-B2D0-001A649D44BD.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/54F8E613-E9C6-E811-AC4D-001A649D5025.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/E4A94CD0-EEC6-E811-89F0-001A647A9506.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/340A78A8-EAC6-E811-A0C1-001A649D48A1.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/CC0B0DEE-EEC6-E811-BD4E-001A649D4ED1.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/F41C87D5-EFC6-E811-90FB-001A649D4E41.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/0A064D6A-F0C6-E811-B803-001A649D4815.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/BA2D0B74-F6C6-E811-BCD9-001A647A94E6.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/F6DEBDE9-E5C6-E811-A970-70106F9D5F90.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/2C7F3AEE-E3C6-E811-B7CF-001A647A98C2.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/DA90B94C-C9C6-E811-8B07-00215E4024C0.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/5C9C0A55-CEC6-E811-810F-001A649D4F15.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/2C95A324-CAC6-E811-86F4-001A649D4E11.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/CC3A2620-CAC6-E811-91DE-001A649D473D.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/18BD579A-CDC6-E811-AFDE-001A649D4C0D.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/08239A0A-CAC6-E811-9C4B-001A649D4A45.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/C0C7EC7C-D0C6-E811-BE68-001A647A94D2.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/8099E063-D2C6-E811-B2B9-001A647AE41A.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/C820C326-D6C6-E811-8650-001A649D4D69.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/E8AB22C0-D7C6-E811-8EF9-001A649D4925.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/D8A342DF-DDC6-E811-8614-001A64996C18.root', 
        '/store/mc/RunIISummer16MiniAODv3/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/270000/B84CB0F2-E2C6-E811-BC6F-001A649D4631.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:5236'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# process.NANOEDMAODSIMoutput = cms.OutputModule("PoolOutputModule",
    # compressionAlgorithm = cms.untracked.string('LZMA'),
    # compressionLevel = cms.untracked.int32(9),
    # dataset = cms.untracked.PSet(
        # dataTier = cms.untracked.string('NANOAODSIM'),
        # filterName = cms.untracked.string('')
    # ),
    # fileName = cms.untracked.string('file:HIG-RunIISummer16NanoAODv4-00121.root'),
    # outputCommands = process.NANOAODSIMEventContent.outputCommands
# )
process.out = cms.OutputModule("NanoAODOutputModule",
    fileName = cms.untracked.string('nano.root'),
    outputCommands = process.NanoAODEDMEventContent.outputCommands,
    compressionLevel = cms.untracked.int32(9),
    # compressionAlgorithm = cms.untracked.string("LZMA"),
    fakeNameForCrab =cms.untracked.bool(True),
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_mcRun2_asymptotic_v6', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
# process.NANOEDMAODSIMoutput_step = cms.EndPath(process.NANOEDMAODSIMoutput)
process.NANOEDMAODSIMoutput_step = cms.EndPath(process.out)  

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOEDMAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
# associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(2)
process.options.numberOfStreams=cms.untracked.uint32(0)
process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

process.particleLevelSequence.remove(process.genParticles2HepMCHiggsVtx);process.particleLevelSequence.remove(process.rivetProducerHTXS);process.particleLevelTables.remove(process.HTXSCategoryTable)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
