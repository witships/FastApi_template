# model.py 名前は何でもOK
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

# ここからほぼ固定で書く～
SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"  # dbファイルは自由
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()
# ～ここまで


# ここから自由にテーブル定義
class Todo(Base):
    __tablename__ = "todos"
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(200))
    done = Column("done", Boolean, default=False)


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(200))
    able = Column("done", Boolean, default=False)


# テーブル作成 ↑のクラスを見てDBとテーブルが作られる
Base.metadata.create_all(bind=engine)
