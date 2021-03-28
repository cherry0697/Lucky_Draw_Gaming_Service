import sqlite3

conn = sqlite3.connect("Event_Details.db")
print("Opened")

conn.execute("create table info (Date text,Time text,Prize Text,Used int)")

print("Table")

conn.close()
