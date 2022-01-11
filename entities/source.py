import sqlite3

from contextlib import contextmanager

@contextmanager
def execute(sql, args=()):
    con = sqlite3.connect('/app/features.db')
    cur = con.cursor() 
    cur.execute(sql, args)
    yield (cur, con)
    con.close()

class Source:
    @staticmethod
    def all():
        with execute("SELECT id, name, location FROM source") as (cur, con):
            return cur.fetchall()

    def insert(self, **args):
        with execute("INSERT INTO source (name, location) VALUES (?, ?)", (args["name"], args["location"])) as (cur, con):
            con.commit()