import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ODM(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ODM
    """
    
    FileType = Model.Attribute()

    AdminData = Model.ManyElements()

    ClinicalData = Model.ManyElements()

    
