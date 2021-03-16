from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine("postgresql://dev:dev@localhost:5432/users", future=True)
metadata = MetaData()
table = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("password", String(64), nullable=False),
    Column("email", String(255)),
    Column("url", String(255)),
)
table.drop(engine)
table.create(engine)
