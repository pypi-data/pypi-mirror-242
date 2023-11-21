import cjen

from cjen.nene.helper import FileHelper

from pyodm.core.resource.database_resource import DataBaseResource
from pyodm.unit_tests.test_forest_factory.mappers.subject_mapper import SubjectMapper


class SubjectDataResource(DataBaseResource):

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
