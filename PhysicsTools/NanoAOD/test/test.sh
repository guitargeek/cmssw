COND=102X_upgrade2018_realistic_v15
ERA=Run2_2018,run2_nanoAOD_102Xv1
W=mc; DQMPD=RelVal_MC102X_TTbar
DQMRUN=1; DQMRRR="R000000001"
DQMTYPE="offline_relval"
OPTS=" -s NANO${DQMSEQ} --$W --eventcontent NANOAODSIM${DQMEC} --datatier NANOAODSIM${DQMDT}  --conditions $COND  --nThreads 4 --era $ERA"
NEVOUT=1000
cmsDriver.py mc102X $OPTS -n $NEVOUT --fileout nano.root --filein /store/mc/RunIIAutumn18MiniAOD/WWZ_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/100000/BAE90A1F-7A73-AB48-80BB-18E065183E22.root

