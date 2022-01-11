import sqlite3
#https://docs.python.org/3/library/sqlite3.html

con = sqlite3.connect('features.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE source
               (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name text, location text)''')

import shutil

shutil.copyfile("db/seeds/data/BostonHousing.csv", "data/BostonHousing.csv")

csv_data = {
    "Boston": "data/BostonHousing.csv"
}

for k, v in csv_data.items():
    cur.execute("INSERT INTO source (name, location) VALUES (?, ?)", (k,v))

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()