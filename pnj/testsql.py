import sqlite3

conn = sqlite3.connect('PNJs.db')
c = conn.cursor()

c.execute("SELECT * FROM pnj")
pnjs = c.fetchall()


for i in pnjs:
    print(i)

conn.close()