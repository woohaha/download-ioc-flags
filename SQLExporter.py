from typing import List, TextIO


class SQLExporter:
    tableName = ''
    fields = []

    def __init__(self, sqlFile: TextIO, tableName: str, fields: List[str]):
        self.file = sqlFile
        self.tableName = tableName
        self.fields = fields

    def writerow(self, row: List):
        fields_str = ','.join([f"`{field}`" for field in self.fields])
        data = ','.join([f"'{field}'" for field in row])

        statement = f'insert into {self.tableName} ({fields_str}) values ({data});'
        self.file.write(statement)
