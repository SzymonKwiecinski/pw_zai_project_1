import sqlmodel
from sqlmodel import create_engine, Field, SQLModel, Session, select
import psycopg2
# default
# engine = create_engine("postgresql://scott:tiger@localhost/mydatabase")

conn = psycopg2.connect(
    host="127.0.0.1",
    database="timeline_app_db",
    user="postgres",
    password="postgres",
    port="2022"
)

cur = conn.cursor()
print('PostgreSQL database version:')
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)
cur.close()

# class test_table(SQLModel, table=True):
#     id: int = Field(primary_key=True)
#     name: str
#
#
# url = "postgresql://postgres:postgres@127.0.0.1:2022/timeline_app_db"
# engine = create_engine(url, echo=True)
#
# def select_heroes():
#     with Session(engine) as session:
#         statement = select(test_table).where(test_table.name == 'szymon')
#         res = session.exec(statement)
#         for x in res:
#             print(x)
#
# select_heroes()
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)