from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.future import select


class Users:
    def __init__(self):
        self.engine = create_engine(
            "postgresql://dev:dev@localhost:5432/users", future=True
        )
        self.metadata = MetaData()
        self.table = Table(
            "users",
            self.metadata,
            Column("user_id", Integer, primary_key=True),
            Column("username", String(50), nullable=False, unique=True),
            Column("password", String(64), nullable=False),
            Column("email", String(255)),
            Column("url", String(255)),
            autoload_with=self.engine,
        )

    def get_login(self, username):
        statement = select(self.table).where(self.table.c.username == username).limit(1)
        with self.engine.connect() as conn:
            result = conn.execute(statement)
            row = result.fetchone()
        return {"user": row["user"], "password": row["123"]}

    def get_URL(self, username):
        statement = select(self.table).where(self.table.c.username == username).limit(1)
        with self.engine.connect() as conn:
            result = conn.execute(statement)
            row = result.fetchone()
        return row["url"]
