import cjen
from cjen import MetaMysql

from pyodm.tests.sql_to_odm.cdisc import CdiscSQL
from pyodm.tests.sql_to_odm.cdisc_element import CdiscElement
from pyodm.utils.path_utils import PathUtils


# @Mapper(map_file="yyyy")
@CdiscSQL(sql_path=PathUtils.folder("pyodm", __file__).joinpath("unit_tests", "sql_to_odm", "sqls", "subjects.sql"),
          mapper_path=PathUtils.folder("pyodm", __file__).joinpath("unit_tests", "sql_to_odm", "mappers", "mapper.xml"))
class SubjectMapper(MetaMysql): ...
# SubjectData = CdiscElement(name="SubjectData", root=True, SubjectKey="SubjectKey")
# StudyEventData = CdiscElement(name="StudyEventData", StudyEventOID="StudyEventOID")
# SiteRef = CdiscElement(name="SiteRef", LocationOID="LocationOID")
# ItemGroupData = CdiscElement(name="ItemGroupData", ItemGroupOID="ItemGroupOID", ItemGroupRepeatKey="ItemGroupRepeatKey")
# ItemData = CdiscElement(name="ItemData", ItemOID="ItemOID")
# Value = CdiscElement(name="Value", SeqNum="SeqNum", Text="Text")

# @cjen.operate.common.value
# def SubjectKey(self): ...
#
# @cjen.operate.common.value
# def StudyEventOID(self): ...
#
# @cjen.operate.common.value
# def ItemGroupOID(self): ...
#
# @cjen.operate.common.value
# def ItemGroupRepeatKey(self): ...
#
# @cjen.operate.common.value
# def ItemOID(self): ...
#
# @cjen.operate.common.value
# def SeqNum(self): ...
#
# @cjen.operate.common.value
# def Text(self): ...
#
# @cjen.operate.common.value
# def LocationOID(self): ...
