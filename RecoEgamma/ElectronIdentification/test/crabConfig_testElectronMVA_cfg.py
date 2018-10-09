from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.psetName = 'testElectronMVA_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = []

config.section_('Data')

# config.General.requestName = "testElectronMVA2016"
# config.Data.inputDataset = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM"

config.General.requestName = "testElectronMVA2017"
config.Data.inputDataset = "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM"

# config.General.requestName = "testElectronMVA2018"
# config.Data.inputDataset = "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v2/MINIAODSIM"

config.Data.inputDBS = 'global'
config.Data.outLFNDirBase = '/store/user/rembserj'

config.Data.totalUnits = -1
config.Data.unitsPerJob = 30
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.allowNonValidInputDataset = True

config.section_('User')

config.section_('Site')

config.Site.storageSite = 'T2_FR_GRIF_LLR'
