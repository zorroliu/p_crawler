# -*- coding: utf-8 -*-

from enum import Enum


class ProcessingType(Enum):
    """
    ProcessType
    """
    NOTHING = 0
    TO_CSV = 1
    TO_SQL = 2


class DataProcessing:
    """
    DataProcessing
    """

    def __init__(self, processing_type: ProcessingType = ProcessingType.NOTHING):
        self.processing_type = processing_type

    def process(self):
        pass


class DataProcessingFactory:
    """
    DataProcessingFactory
    """

    @staticmethod
    def create(processing_type: ProcessingType):
        if processing_type == ProcessingType.TO_CSV:
            return ToCSVProcessing()
        elif processing_type == ProcessingType.TO_SQL:
            return ToSQLProcessing()
        else:
            return DataProcessing()


class ToCSVProcessing(DataProcessing):
    """
    ToCSVProcessing
    """

    def __init__(self, csv_header=None):
        super(ToCSVProcessing, self).__init__(ProcessingType.TO_CSV)
        if csv_header is None:
            csv_header = []
        self.csv_hearer = csv_header

    def process(self):
        pass


class ToSQLProcessing(DataProcessing):
    """
    ToSQLProcessing
    """

    def __init__(self, sql: str = None):
        super(ToSQLProcessing, self).__init__(ProcessingType.TO_SQL)
        self._sql = sql
        self._process_data = []

    def sql(self, sql):
        self._sql = sql
        return self

    def process(self):
        pass


if __name__ == "__main__":
    DataProcessingFactory.create(ProcessingType.TO_SQL).sql("13").process()
    pass
