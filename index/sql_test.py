import sqlite3

conn = sqlite3.connect('library.db')

c = conn.cursor()

c.execute("SELECT count(*) from book")

x=c.fetchone()[0]
print(x)
conn.commit()

conn.close()