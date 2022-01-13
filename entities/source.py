import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
import os
import pandas as pd

@contextmanager
def execute(sql, args=()):
    root = os.environ["DATABASE_ROOT"]
    con = sqlite3.connect(os.path.join(root,'features.db'))
    cur = con.cursor() 
    cur.execute(sql, args)
    yield (cur, con)
    con.close()

@dataclass
class Source:
    id: int
    name: str
    location: str
    type: str

    @classmethod
    def all(cls):
        with execute("SELECT id, name, location, type FROM source") as (cur, con):
            return [cls._row_to_obj(row) for row in cur.fetchall()]

    @staticmethod
    def insert(**args):
        with execute("INSERT INTO source (name, location, type) VALUES (?, ?, ?)", (args["name"], args["location"], args["type"])) as (cur, con):
            con.commit()

    @classmethod
    def find_by_id(cls, id):
        with execute("SELECT id, name, location, type FROM source WHERE id = ?", (id,)) as (cur, con):
            row = cur.fetchone()
            return cls._row_to_obj(row)

    @staticmethod
    def _row_to_obj(row):
        if row[3] == "csv":
            return Source(id=row[0], name=row[1], location=row[2], type=row[3])
        elif row[3] == "sqlite":
            return SqlSource(id=row[0], name=row[1], location=row[2])

    def dataframe(self):
        return pd.read_csv(self.location)

@dataclass
class SqlSource:
    id: int
    name: str
    location: str

    def dataframe(self):
        #FIXME: don't hardcore the values
        cnx = sqlite3.connect("data/iris.sqlite")
        return pd.read_sql_query("SELECT * FROM iris", cnx)

