import sqlite3

conn = sqlite3.Connection("data.db")
cur = conn.cursor()

create_table = "CREATE TABLE users (id int, username text,password text)"
cur.execute(create_table)

user = (1, "suresh60", "password")

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cur.execute(insert_query,user)

users = [
    (2,"sriram93","password"),
    (3,"vijji63","password")
]

cur.executemany(insert_query,users)

select_query = "SELECT * FROM users"

for row in cur.execute(select_query):
    print(row)

conn.commit()
conn.close()