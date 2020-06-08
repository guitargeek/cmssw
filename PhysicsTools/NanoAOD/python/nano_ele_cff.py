from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.electrons_cff import *
from PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff import *

# from Configuration.Eras.Modifier_run2_miniAOD_80XLegacy_cff import run2_miniAOD_80XLegacy
# from Configuration.Eras.Modifier_run2_nanoAOD_94X2016_cff import run2_nanoAOD_94X2016
# from Configuration.Eras.Modifier_run2_nanoAOD_94XMiniAODv1_cff import run2_nanoAOD_94XMiniAODv1
# from Configuration.Eras.Modifier_run2_nanoAOD_94XMiniAODv2_cff import run2_nanoAOD_94XMiniAODv2
# from Configuration.Eras.Modifier_run2_nanoAOD_102Xv1_cff import run2_nanoAOD_102Xv1

nanoSequence = cms.Sequence(electronSequence + electronTables)
