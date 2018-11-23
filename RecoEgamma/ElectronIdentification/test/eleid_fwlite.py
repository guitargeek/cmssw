import ROOT
ROOT.gROOT.SetBatch()

import numpy as np

from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import EleMVA_6CategoriesCuts, mvaVariablesFile
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff import mvaWeightFiles

class ElectronMVAID:

    def __init__(self, name, tag, flavor, xmls):
        self.name = name
        self.tag = tag
        self.flavor = flavor
        self.sxmls = ROOT.vector(ROOT.string)()
        for x in xmls: self.sxmls.push_back(x)
        self._init = False

    def __call__(self, ele, convs, beam_spot, rho, debug=False):
        if not self._init:
            print('initializing electron mva id')
            ROOT.gSystem.Load("libRecoEgammaElectronIdentification")
            debug = False
            categoryCutStrings =  ROOT.vector(ROOT.string)()
            for x in EleMVA_6CategoriesCuts : 
                categoryCutStrings.push_back(x)
            self.estimator = ROOT.ElectronMVAEstimatorRun2(
                self.tag, self.name, len(self.sxmls), 
                mvaVariablesFile, categoryCutStrings, debug
                )
            self.estimator.init(self.sxmls)
            self._init = True
        extra_vars = self.estimator.getExtraVars(ele, convs, beam_spot, rho[0])
        return self.estimator.mvaValue(ele, extra_vars)

eleid_Fall17IsoV2 = ElectronMVAID(
    "ElectronMVAEstimatorRun2Fall17V2","V2","Iso", mvaWeightFiles
)

from DataFormats.FWLite import Events, Handle

print('open input file...')

events = Events('root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/RECOSIMstep_94X_mc2017_realistic_v10-v1/00000/0293A280-B5F3-E711-8303-3417EBE33927.root')

ele_handle  = Handle('std::vector<pat::Electron>')
rho_handle  = Handle('double')
conv_handle = Handle('reco::ConversionCollection')
bs_handle   = Handle('reco::BeamSpot')

print('start processing')
accepted = 0
for i,event in enumerate(events): 

    if i == 100:
        break

    event.getByLabel(('slimmedElectrons'),                 ele_handle)
    event.getByLabel(('fixedGridRhoFastjetAll'),           rho_handle)
    event.getByLabel(('reducedEgamma:reducedConversions'), conv_handle)
    event.getByLabel(('offlineBeamSpot'),                  bs_handle)

    electrons = ele_handle.product()
    convs     = conv_handle.product()
    beam_spot = bs_handle.product()
    rho       = rho_handle.product()

    for ele in electrons:
        mva = eleid_Fall17IsoV2(ele, convs, beam_spot, rho)
        print(mva)
