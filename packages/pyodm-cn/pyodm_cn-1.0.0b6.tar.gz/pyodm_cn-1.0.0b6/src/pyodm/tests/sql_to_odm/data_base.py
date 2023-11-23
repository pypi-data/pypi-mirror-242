import pathlib

import cjen
from cjen.nene.database_info import DataBaseInfo
from cjen.nene.helper import FileHelper

from pyodm.core.resource.database_resource import DataBaseResource
from pyodm.core.xml.writer.cdisc_xml_writer import CdiscXmlWriter
from pyodm.factory.cdsic_xml_xsd_factory import CdiscXMLXsdFactory
from pyodm.tests.sql_to_odm.mappers.subject_mapper import SubjectMapper
from pyodm.tests.sql_to_odm.otree_reader import OtreeReader
from pyodm.utils.forest import Forest
from pyodm.utils.path_utils import PathUtils


class DataBase(DataBaseResource):

    def __init__(self, database_info, registry):
        super().__init__(database_info)
        self.registry = registry

    def load(self):
        return self.subjects()

    @cjen.operate.mysql.factory(
        clazz=SubjectMapper,
        sql=FileHelper.read(SubjectMapper.sql_file),
        size=-1
    )
    def subjects(self, subject_mappers: list[SubjectMapper] = None, **kwargs):
        return [subject_mapper.mapper(self.registry) for subject_mapper in subject_mappers]

        # return []
        # return [
        #     [dict(SubjectData=dict(SubjectKey=subject_mapper.SubjectKey())),
        #      dict(StudyEventData=dict(StudyEventOID=subject_mapper.StudyEventOID()),
        #           SiteRef=dict(LocationOID=subject_mapper.LocationOID())),
        #      dict(ItemGroupData=dict(ItemGroupOID=subject_mapper.ItemGroupOID(),
        #                              ItemGroupRepeatKey=subject_mapper.ItemGroupRepeatKey())),
        #      dict(ItemData=dict(ItemOID=subject_mapper.ItemOID())),
        #      dict(Value=dict(SeqNum=subject_mapper.SeqNum(), Text=subject_mapper.Text()))
        #      ] for subject_mapper in subject_mappers
        # ]

    def data(self) -> list[list[dict]]:
        return self.subjects()


def xsd_files():
    base = PathUtils.folder("pyodm", __file__).joinpath("model", "v2", "resources", "schema")
    xsds = ["ODM-admindata.xsd", "ODM-clinicaldata.xsd", "ODM-foundation.xsd",
            "ODM-protocol.xsd", "ODM-referencedata.xsd", "ODM-study.xsd"]
    return [base.joinpath(xsd) for xsd in xsds]


if __name__ == '__main__':
    registry = CdiscXMLXsdFactory(data_file=pathlib.Path(""), xsd_files=xsd_files())
    registry.clazz_reader()
    dbc = DataBase(DataBaseInfo.factory(
        dict(host="dev-03.cluster-c9qe4y0vrvda.rds.cn-northwest-1.amazonaws.com.cn", port=3306,
             user='root', pwd='8YTJWOuA7XRK17wRQnw4',
             database='eclinical_edc_dev_846')), registry)
    # dbc.subjects()

    otree = Forest.transform(dbc.data())

    # registry = CdiscSpecificationFactory(data_file=pathlib.Path(""), specification_files=["SpecificationV2.xml"])
    registry.clazz_reader()
    reader = OtreeReader(registry)
    objs = reader.read_data(otree)
    i = 1
    for obj in objs:
        cw = CdiscXmlWriter(obj, pathlib.Path(f"test{i}.xml"))
        cw.write()
        i += 1
