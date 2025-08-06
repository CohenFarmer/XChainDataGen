import sqlalchemy
from sqlalchemy import text

engine = sqlalchemy.create_engine("postgresql://admin:pwd@localhost/across")
conn = engine.connect()
print(conn.execute(text("SELECT 1")).fetchall())