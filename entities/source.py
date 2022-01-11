import sqlite3

from contextlib import contextmanager
from dataclasses import dataclass

@contextmanager
def execute(sql, args=()):
    con = sqlite3.connect('/app/features.db')
    cur = con.cursor() 
    cur.execute(sql, args)
    yield (cur, con)
    con.close()

@dataclass
class Source:
    id: int
    name: str
    location: str

    @classmethod
    def all(cls):
        with execute("SELECT id, name, location FROM source") as (cur, con):
            return [cls._row_to_obj(row) for row in cur.fetchall()]

    @staticmethod
    def insert(self, **args):
        with execute("INSERT INTO source (name, location) VALUES (?, ?)", (args["name"], args["location"])) as (cur, con):
            con.commit()

    @classmethod
    def find_by_id(cls, id):
        with execute("SELECT id, name, location FROM source WHERE id = ?", (id,)) as (cur, con):
            row = cur.fetchone()
            return cls._row_to_obj(row)

    @staticmethod
    def _row_to_obj(row):
        return Source(id=row[0], name=row[1], location=row[2])