from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'nano6'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'nano_WWZ_2016_cfg.py'
config.JobType.outputFiles = ['nano.root']

config.Data.inputDataset = '/WWZJetsTo4L2Nu_4f_TuneCUETP8M1_13TeV_aMCatNLOFxFx_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2000
config.Data.totalUnits = 6000
config.Data.outLFNDirBase = "/store/user/rembserj/MultileptonAnalysis/NANOAOD"
config.Data.outputDatasetTag = 'NanoTest2'



config.Data.publication                = False
config.Data.allowNonValidInputDataset  = True
config.JobType.allowUndistributedCMSSW = True

config.Site.storageSite = 'T2_FR_GRIF_LLR'
