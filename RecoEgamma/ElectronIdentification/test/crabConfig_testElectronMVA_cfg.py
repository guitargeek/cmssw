from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.psetName = 'testElectronMVA_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = []

config.section_('Data')

config.General.requestName = "egamma_paper"
config.Data.inputDataset = "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM"

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
