import json
import sqlite3
from anlogger import Logger as AnLogger
from logging import Logger
from pydantic import BaseModel, create_model
from typing import Dict, List, Optional
from ansqlite.schema import TableColumn, PrimaryKeyType
from ansqlite.utils import trace


class Database:
    def __init__(
        self,
        database_path: str,
        schemas: Dict[str, List[TableColumn]] = {},
        logger: Optional[Logger] = None
    ):
        super().__init__()
        self.logger = logger if logger is not None else AnLogger(
            name='ansqlite', default_loglevel='INFO').get()

        self.schemas: Dict[str, List[TableColumn]] = {}
        self.models: Dict[str, BaseModel] = {}

        try:
            self.dbconn = sqlite3.connect(database_path)
        except Exception as e:
            self.logger.error(trace('Failed to open database', e))
            self.dbconn = None

        for k, v in schemas.items():
            self.init_table(table_name=k, table_schema=v)

    def init_table(self, table_name: str, table_schema: List[TableColumn]) -> bool:
        column_sql = []
        model_entries = {}
        schema = [TableColumn.model_validate(col) for col in table_schema]

        def pk_desc(x: TableColumn) -> str:
            return ' DESC' if x.primary_key is PrimaryKeyType.Descending else ''
        pk_cols = [
            f'{x.name}{pk_desc(x)}' for x in schema if x.primary_key is not None]
        pk_text = f'PRIMARY KEY ({", ".join(pk_cols)})' if len(
            pk_cols) > 0 else None

        for col in schema:
            not_nullable = col.nullable is False
            s = [
                col.name,
                col.datatype.name
            ]
            if (col.primary_key is None):
                if not_nullable is True:
                    s.append('NOT NULL')
                if col.unique is True:
                    s.append('UNIQUE')
            column_sql.append(' '.join(s))
            model_entries[col.name] = (
                col.datatype.value, ... if not_nullable else None)

        if pk_text is not None:
            column_sql.append(pk_text)

        self.models[table_name] = create_model(table_name, **model_entries)

        try:
            cur = self.dbconn.cursor()
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(column_sql)});')
            self.schemas[table_name] = table_schema

        except Exception as e:
            self.logger.error(trace('Failed to initialize table', e))
            self.dbconn = None

    def check_connection(self) -> bool:
        return self.dbconn is not None

    def get_connection(self) -> sqlite3.Connection:
        return self.dbconn

    def insert_data(
        self,
        table_name: str,
        data: List[BaseModel],
    ) -> None:
        if len(data) < 1:
            return

        self.logger.debug(
            f'Save data to table {table_name}: {json.dumps(data, indent=2)}')

        schema = self.schemas[table_name] if table_name in self.schemas else None
        if schema is None:
            raise Exception(
                f'Table {table_name} has not been initialized; saving data failed')

        model = self.models[table_name]

        cols = model.model_validate(data[0]).model_dump().keys()
        rowdata = [tuple(model.model_validate(row).model_dump().values())
                   for row in data]

        try:
            cur = self.dbconn.cursor()
            cur.executemany(
                f"INSERT OR IGNORE INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join('?'*len(cols))})", rowdata)
            self.dbconn.commit()
        except Exception as e:
            self.logger.error(trace('Failed to save data', e))
            raise e

    def execute_and_fetchall(self, sql: str, errmsg: str) -> List[Dict] | None:
        try:
            cur = self.dbconn.cursor()
            res = cur.execute(sql)
            rows = res.fetchall()
            cols = [description[0] for description in cur.description]
            data = [dict(zip(cols, row)) for row in rows]
            return data
        except Exception as e:
            self.logger.error(trace(errmsg, e))
            raise e

    def execute_and_commit(self, sql: str, errmsg: str) -> None:
        try:
            cur = self.dbconn.cursor()
            cur.execute(sql)
            self.dbconn.commit()
        except Exception as e:
            self.logger.error(trace(errmsg, e))
            raise e
