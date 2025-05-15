from sqlalchemy import Column, Integer, String, DateTime, func

from database.mysql_client import Base


class ExampleTable(Base):
    __tablename__ = "example_table"

    id = Column(String(32), primary_key=True, comment="uuid 主键")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
