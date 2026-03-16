import sqlite3
import pandas as pd

conn = sqlite3.connect('shekinah_choir.db')

print("=== TABLES ===")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

print("\n=== MEMBRES COUNT ===")
count = pd.read_sql_query("SELECT COUNT(*) as count FROM membres;", conn)
print(count)

print("\n=== MEMBRES SAMPLE ===")
sample = pd.read_sql_query("SELECT * FROM membres LIMIT 5;", conn)
print(sample)

print("\n=== SCHEMA MEMBRES ===")
schema = pd.read_sql_query("PRAGMA table_info(membres);", conn)
print(schema)

print("\n=== FINANCES SAMPLE ===")
fin = pd.read_sql_query("SELECT * FROM finances LIMIT 5;", conn)
print(fin)

conn.close()
print("✅ Inspection terminée!")

