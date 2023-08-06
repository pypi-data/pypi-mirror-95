"""Utilities for the creation and work with comp models.

Simplifies the port linking, submodel generation, ...

Heavily used in the dynamic FBA simulator. Mainly in the model creation
process. But the flattening parts also during the simulation
of the dynamic FBA models.
"""

import logging
from typing import List

import libsbml

import sbmlutils.factory as factory


logger = logging.getLogger(__name__)


def create_ExternalModelDefinition(doc_comp, emd_id, source):
    """Create comp ExternalModelDefinition.

    :param doc_comp: SBMLDocument comp plugin
    :param emd_id: id of external model definition
    :param source: source
    :return:
    """
    extdef = doc_comp.createExternalModelDefinition()
    extdef.setId(emd_id)
    extdef.setName(emd_id)
    extdef.setModelRef(emd_id)
    extdef.setSource(source)
    return extdef


def add_submodel_from_emd(
    model_comp: libsbml.CompModelPlugin,
    submodel_id,
    emd: libsbml.ExternalModelDefinition,
):
    """Add submodel to the model from given ExternalModelDefinition.

    :param model_comp: Model comp plugin
    :param submodel_id:
    :param emd:
    :return:
    """

    model_ref = emd.getModelRef()
    submodel = model_comp.createSubmodel()
    submodel.setId(submodel_id)
    submodel.setModelRef(model_ref)

    model_comp = emd.getReferencedModel()
    if model_comp and model_comp.isSetSBOTerm():
        submodel.setSBOTerm(model_comp.getSBOTerm())
    return submodel


def get_submodel_frameworks(doc):
    """Read the SBO terms of the submodels.

    These are used to distinguish the different frameworks of the submodels.
    :param doc:
    :return:
    """
    frameworks = {}
    # get list of submodels
    model = doc.getModel()
    mplugin = model.getPlugin("comp")

    # model.setSBOTerm(comp.SBO_CONTINOUS_FRAMEWORK)
    for submodel in mplugin.getListOfSubmodels():
        sid = submodel.getId()
        sbo = None
        if submodel.isSetSBOTerm():
            # This is the sbo which is set on the submodel element
            # not the SBO which is set on the model in listOfModels or
            # listOfExternalModels
            sbo = submodel.getSBOTerm()
        frameworks[sid] = {"sid": sid, "modelRef": submodel.getModelRef(), "sbo": sbo}

    return frameworks


class ExternalModelDefinition(factory.Sbase):
    """ExternalModelDefinition."""

    def __init__(
        self, sid, source, modelRef, md5=None, name=None, sboTerm=None, metaId=None
    ):
        """Create an ExternalModelDefinition."""
        super(ExternalModelDefinition, self).__init__(
            sid=sid, name=name, sboTerm=sboTerm, metaId=metaId
        )
        self.source = source
        self.modelRef = modelRef
        self.md5 = md5

    def create_sbml(self, model: libsbml.Model) -> libsbml.ExternalModelDefinition:
        """Create ExternalModelDefinition."""
        doc = model.getSBMLDocument()
        cdoc = doc.getPlugin("comp")
        extdef = cdoc.createExternalModelDefinition()
        self.set_fields(extdef)
        return extdef

    def set_fields(self, obj: libsbml.ExternalModelDefinition) -> None:
        """Set fields on ExternalModelDefinition."""
        super(ExternalModelDefinition, self).set_fields(obj)
        obj.setModelRef(self.modelRef)
        obj.setSource(self.source)
        if self.md5 is not None:
            obj.setMd5(self.md5)


class Submodel(factory.Sbase):
    """Submodel."""

    def __init__(
        self,
        sid,
        modelRef=None,
        timeConversionFactor=None,
        extentConversionFactor=None,
        name=None,
        sboTerm=None,
        metaId=None,
    ):
        """Create a Submodel."""
        super(Submodel, self).__init__(
            sid=sid, name=name, sboTerm=sboTerm, metaId=metaId
        )
        self.modelRef = modelRef
        self.timeConversionFactor = timeConversionFactor
        self.extentConversionFactor = extentConversionFactor

    def create_sbml(self, model: libsbml.Model) -> libsbml.Submodel:
        """Create SBML Submodel."""
        cmodel = model.getPlugin("comp")
        submodel = cmodel.createSubmodel()
        self.set_fields(submodel)

        submodel.setModelRef(self.modelRef)
        if self.timeConversionFactor:
            submodel.setTimeConversionFactor(self.timeConversionFactor)
        if self.extentConversionFactor:
            submodel.setExtentConversionFactor(self.extentConversionFactor)

        return submodel

    def set_fields(self, obj: libsbml.Submodel):
        """Set fields on Submodel."""
        super(Submodel, self).set_fields(obj)


class SbaseRef(factory.Sbase):
    """SBaseRef."""

    def __init__(
        self,
        sid,
        portRef=None,
        idRef=None,
        unitRef=None,
        metaIdRef=None,
        name=None,
        sboTerm=None,
        metaId=None,
    ):
        """Create an SBaseRef."""
        super(SbaseRef, self).__init__(
            sid=sid, name=name, sboTerm=sboTerm, metaId=metaId
        )
        self.portRef = portRef
        self.idRef = idRef
        self.unitRef = unitRef
        self.metaIdRef = metaIdRef

    def set_fields(self, obj: libsbml.SBaseRef) -> None:
        """Set fields on SBaseRef."""
        super(SbaseRef, self).set_fields(obj)

        obj.setId(self.sid)
        if self.portRef is not None:
            obj.setPortRef(self.portRef)
        if self.idRef is not None:
            obj.setIdRef(self.idRef)
        if self.unitRef is not None:
            unit_str = factory.Unit.get_unit_string(self.unitRef)
            obj.setUnitRef(unit_str)
        if self.metaIdRef is not None:
            obj.setMetaIdRef(self.metaIdRef)


class ReplacedElement(SbaseRef):
    """ReplacedElement."""

    def __init__(
        self,
        sid,
        elementRef,
        submodelRef,
        deletion=None,
        conversionFactor=None,
        portRef=None,
        idRef=None,
        unitRef=None,
        metaIdRef=None,
        name=None,
        sboTerm=None,
        metaId=None,
    ):
        """Create a ReplacedElement."""
        super(ReplacedElement, self).__init__(
            sid=sid,
            portRef=portRef,
            idRef=idRef,
            unitRef=unitRef,
            metaIdRef=metaIdRef,
            name=name,
            sboTerm=sboTerm,
            metaId=metaId,
        )
        self.elementRef = elementRef
        self.submodelRef = submodelRef
        self.deletion = deletion
        self.conversionFactor = conversionFactor

    def create_sbml(self, model: libsbml.Model) -> libsbml.ReplacedElement:
        """Create SBML ReplacedElement."""
        # resolve port element
        e = model.getElementBySId(self.elementRef)
        if not e:
            # fallback to units (only working if no name shadowing)
            e = model.getUnitDefinition(self.elementRef)
            if not e:
                raise ValueError(
                    f"Neither SBML element nor UnitDefinition found for elementRef: "
                    f"'{self.elementRef}' in '{self}'"
                )

        eplugin = e.getPlugin("comp")
        obj = eplugin.createReplacedElement()
        self.set_fields(obj)

        return obj

    def set_fields(self, obj: libsbml.ReplacedElement) -> None:
        """Set fields on ReplacedElement."""
        super(ReplacedElement, self).set_fields(obj)
        obj.setSubmodelRef(self.submodelRef)
        if self.deletion:
            obj.setDeletion(self.deletion)
        if self.conversionFactor:
            obj.setConversionFactor(self.conversionFactor)


class Deletion(SbaseRef):
    """Deletion."""

    def __init__(
        self,
        sid,
        submodelRef,
        portRef=None,
        idRef=None,
        unitRef=None,
        metaIdRef=None,
        name=None,
        sboTerm=None,
        metaId=None,
    ):
        """Initialize Deletion."""
        super(Deletion, self).__init__(
            sid=sid,
            portRef=portRef,
            idRef=idRef,
            unitRef=unitRef,
            metaIdRef=metaIdRef,
            name=name,
            sboTerm=sboTerm,
            metaId=metaId,
        )
        self.submodelRef = submodelRef

    def create_sbml(self, model: libsbml.Model) -> libsbml.Deletion:
        """Create SBML Deletion."""
        # Deletions for submodels
        cmodel = model.getPlugin("comp")  # type: libsbml.CompModelPlugin
        submodel = cmodel.getSubmodel(self.submodelRef)  # type: libsbml.Submodel
        deletion = submodel.createDeletion()  # type: libsbml.Deletion
        self.set_fields(deletion)

        return deletion

    def set_fields(self, obj: libsbml.Deletion):
        """Set fields on Deletion."""
        super(Deletion, self).set_fields(obj)


##########################################################################
# Ports
##########################################################################
# Ports are stored in an optional child ListOfPorts object, which, if
# present, must contain one or more Port objects.  All of the Ports
# present in the ListOfPorts collectively define the 'port interface' of
# the Model.
PORT_TYPE_PORT = "port"
PORT_TYPE_INPUT = "input port"
PORT_TYPE_OUTPUT = "output port"


class Port(SbaseRef):
    """Port."""

    def __init__(
        self,
        sid,
        portRef=None,
        idRef=None,
        unitRef=None,
        metaIdRef=None,
        portType=PORT_TYPE_PORT,
        name=None,
        sboTerm=None,
        metaId=None,
    ):
        """Create a Port."""
        super(Port, self).__init__(
            sid=sid,
            portRef=portRef,
            idRef=idRef,
            unitRef=unitRef,
            metaIdRef=metaIdRef,
            name=name,
            sboTerm=sboTerm,
            metaId=metaId,
        )
        self.portType = portType

    def create_sbml(self, model: libsbml.Model) -> libsbml.Port:
        """Create SBML for Port."""
        cmodel = model.getPlugin("comp")
        p = cmodel.createPort()
        self.set_fields(p)

        if self.sboTerm is None:
            if self.portType == PORT_TYPE_PORT:
                # SBO:0000599 - port
                sbo = 599
            elif self.portType == PORT_TYPE_INPUT:
                # SBO:0000600 - input port
                sbo = 600
            elif self.portType == PORT_TYPE_OUTPUT:
                # SBO:0000601 - output port
                sbo = 601
            p.setSBOTerm(sbo)

        return p

    def set_fields(self, obj: libsbml.Port) -> None:
        """Set fields on Port."""
        super(Port, self).set_fields(obj)


def create_ports(
    model: libsbml.Model,
    portRefs=None,
    idRefs=None,
    unitRefs=None,
    metaIdRefs=None,
    portType: str = PORT_TYPE_PORT,
    suffix: str = "_port",
) -> List[Port]:
    """Create ports for given model.

    Helper function to create port creation.
    :param model: SBML model
    :param portRefs: dict of the form {pid:portRef}
    :param idRefs: dict of the form {pid:idRef}
    :param unitRefs: dict of the form {pid:unitRef}
    :param metaIdRefs: dict of the form {pid:metaIdRef}

    :return:
    """
    ports = []
    if portRefs is not None:
        ptype = "portRef"
        data = portRefs
    elif idRefs is not None:
        ptype = "idRef"
        data = idRefs
    elif unitRefs is not None:
        ptype = "unitRef"
        data = unitRefs
    elif metaIdRefs is not None:
        ptype = "metaIdRef"
        data = metaIdRefs

    # dictionary, port ids are provided
    if type(data) == dict:
        for pid, ref in data.items():
            kwargs = {"pid": pid, ptype: ref}
            ports.append(_create_port(model, portType=portType, **kwargs))

    # only a list of references, port ids created via suffix appending
    elif type(data) in [list, tuple]:
        for ref in data:
            pid = ref + suffix
            kwargs = {"pid": pid, ptype: ref}
            ports.append(_create_port(model, portType=portType, **kwargs))

    return ports


def _create_port(
    model,
    pid,
    name=None,
    portRef=None,
    idRef=None,
    unitRef=None,
    metaIdRef=None,
    portType=PORT_TYPE_PORT,
):
    """Create port in given model.

    :param model:
    :param pid:
    :param name:
    :param portRef:
    :param idRef:
    :param unitRef:
    :param metaIdRef:
    :param portType:
    :return:
    """
    cmodel = model.getPlugin("comp")
    p = cmodel.createPort()
    p.setId(pid)
    if name is not None:
        p.setName(name)
    ref = None
    if portRef is not None:
        p.setPortRef(portRef)
        ref = portRef
    if idRef is not None:
        p.setIdRef(idRef)
        ref = idRef
    if unitRef is not None:
        unit_str = factory.get_unit_string(unitRef)
        p.setUnitRef(unit_str)
        ref = unit_str
    if metaIdRef is not None:
        p.setMetaIdRef(metaIdRef)
        ref = metaIdRef
    if name is None and ref is not None:
        p.setName("port {}".format(ref))
    if portType == PORT_TYPE_PORT:
        # SBO:0000599 - port
        p.setSBOTerm(599)
    elif portType == PORT_TYPE_INPUT:
        # SBO:0000600 - input port
        p.setSBOTerm(600)
    elif portType == PORT_TYPE_OUTPUT:
        # SBO:0000601 - output port
        p.setSBOTerm(601)

    return p


##########################################################################
# Replacement helpers
##########################################################################
SBASE_REF_TYPE_PORT = "portRef"
SBASE_REF_TYPE_ID = "idRef"
SBASE_REF_TYPE_UNIT = "unitRef"
SBASE_REF_TYPE_METAID = "metIdRef"


def replace_elements(model, sid, ref_type, replaced_elements):
    """Replace elements in comp.

    :param model:
    :param sid:
    :param ref_type:
    :param replaced_elements:
    :return:
    """
    for submodel, rep_ids in replaced_elements.items():
        for rep_id in rep_ids:
            _create_replaced_element(model, sid, submodel, rep_id, ref_type=ref_type)


def replace_element_in_submodels(model, sid, ref_type, submodels):
    """Replace elements submodels with the identical id.

    For instance to replace all the units in the submodels.

    :param model:
    :param sid:
    :param ref_type:
    :param submodels:
    :return:
    """
    for submodel in submodels:
        _create_replaced_element(model, sid, submodel, sid, ref_type=ref_type)


def _create_replaced_element(model, sid, submodel, replaced_id, ref_type):
    """Create a replaced element.

    :param model:
    :param sid:
    :param submodel:
    :param replaced_id:
    :param ref_type:
    :return:
    """
    eplugin = _get_eplugin_by_sid(model, sid)

    # print(sid, '--rep-->', submodel, ':', replaced_id)
    rep_element = eplugin.createReplacedElement()
    rep_element.setSubmodelRef(submodel)
    _set_ref(rep_element, ref_id=replaced_id, ref_type=ref_type)

    return rep_element


def replaced_by(model, sid, ref_type, submodel, replaced_by):
    """replaced_by.

    The element with sid in the model is replaced by the
    replacing_id in the submodel with submodel_id.

    :param model:
    :param sid:
    :param ref_type:
    :param submodel:
    :param replaced_by:
    :return:
    """
    eplugin = _get_eplugin_by_sid(model=model, sid=sid)
    rby = eplugin.createReplacedBy()
    rby.setSubmodelRef(submodel)
    _set_ref(object=rby, ref_id=replaced_by, ref_type=ref_type)


def comp_delete(model):
    """Delete elements from top model.

    :param model:
    :return:
    """
    pass


def _get_eplugin_by_sid(model, sid):
    """Get the comp plugin by sid.

    :param model: SBMLModel instance
    :param sid: SBase id of object
    :return:
    """
    e = model.getElementBySId(sid)
    if not e:
        e = model.getUnitDefinition(sid)
    eplugin = e.getPlugin("comp")
    return eplugin


def _set_ref(object, ref_id, ref_type):
    """Set reference for given reference type in the object.

    Objects can be
        ReplacedBy
        ReplacedElement
    """
    if ref_type == SBASE_REF_TYPE_ID:
        object.setIdRef(ref_id)
    elif ref_type == SBASE_REF_TYPE_UNIT:
        object.setUnitRef(ref_id)
    elif ref_type == SBASE_REF_TYPE_PORT:
        object.setPortRef(ref_id)
    elif ref_type == SBASE_REF_TYPE_METAID:
        object.setMetaIdRef(ref_id)
