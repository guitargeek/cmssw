import os
import sys

import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupVIDSelection, addVIDSelectionToPATProducer


__path__.append(
    os.environ["CMSSW_BASE"]
    + "/cfipython/"
    + os.environ["SCRAM_ARCH"]
    + "/RecoEgamma/ElectronIdentification"
)


def setupEgmGsfElectronIDSequence(
    process,
    identifications=None,
    data_format="MiniAOD",
    electron_collection=None,
    pat_producer=None,
    add_user_data=False,
):

    electron_collection_miniAOD = cms.InputTag("slimmedElectrons")
    electron_collection_AOD = cms.InputTag("dummy")

    if data_format == "MiniAOD":
        if electron_collection is None:
            electron_collection = "slimmedElectrons"
    elif data_format == "AOD":
        if electron_collection is None:
            electron_collection = "gedGsfElectrons"
    else:
        raise ValueError("Unsupported data format: the EGM electron IDs support only MiniAOD and AOD.")

    def to_input_tag(tag):
        if type(tag) != cms.InputTag:
            tag = cms.InputTag(tag)
        return tag

    electron_collection = to_input_tag(electron_collection)

    if data_format == "MiniAOD": electron_collection_miniAOD = electron_collection
    elif data_format == "AOD": electron_collection_AOD = electron_collection

    mvaConfigsForEleProducer = _getMVAProducerParameterSets(identifications)
    needs_mva = len(mvaConfigsForEleProducer) > 0

    process.egmGsfElectronIDs = cms.EDProducer(
        "VersionedGsfElectronIdProducer",
        physicsObjectSrc=electron_collection,
        physicsObjectIDs=cms.VPSet(),
    )

    if needs_mva:
        process.electronMVAValueMapProducer = cms.EDProducer(
            "ElectronMVAValueMapProducer",
            src=electron_collection_AOD,
            srcMiniAOD=electron_collection_miniAOD,
            mvaConfigurations=mvaConfigsForEleProducer,
        )

        process.egmGsfElectronIDTask = cms.Task(process.egmGsfElectronIDs, process.electronMVAValueMapProducer)

    else:
        process.egmGsfElectronIDTask = cms.Task(process.egmGsfElectronIDs)

    process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDTask)

    for idmod in identifications:
        id_module_name = "RecoEgamma.ElectronIdentification.Identification." + idmod + "_cff"
        idmod = __import__(id_module_name, globals(), locals(), ["idName", "cutFlow"])
        for name in dir(idmod):
            item = getattr(idmod, name)
            if hasattr(item, "idName") and hasattr(item, "cutFlow"):
                _setupVIDElectronSelection(
                    process,
                    item,
                    pat_producer,
                    add_user_data,
                    process.egmGsfElectronIDTask,
                    data_format == "MiniAOD"
                )

    if hasattr(process, "process.heepIDVarValueMaps"):
        process.process.heepIDVarValueMaps.eles = electron_collection_AOD
        process.process.heepIDVarValueMaps.elesMiniAOD = electron_collection_AOD

def get_working_points(identification):
    working_points = []

    modname = "RecoEgamma.ElectronIdentification.Identification." + identification + "_cff"
    ids = __import__(modname, globals(), locals(), ['idName','cutFlow'])
    for name in dir(ids):
        _id = getattr(ids,name)
        if hasattr(_id,'idName') and hasattr(_id,'cutFlow'):
            working_points.append(_id.idName.value())

    return working_points


def get_cut_names(identification, working_point):
    modname = "RecoEgamma.ElectronIdentification.Identification." + identification + "_cff"
    ids = __import__(modname, globals(), locals(), ['idName','cutFlow'])
    for name in dir(ids):
        _id = getattr(ids,name)
        if hasattr(_id,'idName') and hasattr(_id,'cutFlow'):
            if _id.idName == working_point:
                return [cut.cutName.value() for cut in _id.cutFlow]

    print("Working point " + working_point + " not found in " + identification + ", returning empty list.")
    return []


def _setupVIDElectronSelection(process, cutflow, patProducer=None, addUserData=True, task=None, useMiniAOD=True):
    if not hasattr(process, "egmGsfElectronIDs"):
        raise Exception("VIDProducerNotAvailable, egmGsfElectronIDs producer not available in process!")

    setupVIDSelection(process.egmGsfElectronIDs, cutflow)

    # add to PAT electron producer if available or specified
    if hasattr(process, "patElectrons") or patProducer is not None:
        if patProducer is None:
            patProducer = process.patElectrons
        idName = cutflow.idName.value()
        addVIDSelectionToPATProducer(patProducer, "egmGsfElectronIDs", idName, addUserData)

    # we know cutflow has a name otherwise an exception would have been thrown in setupVIDSelection
    # run this for all heep IDs except V60 standard for which it is not needed
    # it is needed for V61 and V70
    if (
        cutflow.idName.value().find("HEEP") != -1
        and cutflow.idName.value() != "heepElectronID-HEEPV60"
    ):

        from RecoEgamma.ElectronIdentification.Identification.heepElectronID_tools import addHEEPProducersToSeq

        addHEEPProducersToSeq(
            process=process,
            seq=process.egmGsfElectronIDSequence,
            useMiniAOD=useMiniAOD,
            task=task,
        )


def _getMVAProducerParameterSets(identifications):

    mvaConfigsForEleProducer = cms.VPSet()

    for idmod in identifications:
        if idmod.startswith("mvaElectronID_"):
            full_idmod = "RecoEgamma.ElectronIdentification.Identification." + idmod + "_cff"
            __import__(full_idmod)
            module = sys.modules[full_idmod]
            for name in dir(module):
                item = getattr(module, name)
                if hasattr(item, "mvaName") and hasattr(item, "mvaTag"):
                    mvaConfigsForEleProducer.append(item)

    return mvaConfigsForEleProducer
