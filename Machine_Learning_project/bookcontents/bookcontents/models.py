# import settings
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

class Channels(DeclarativeBase):
    """Sqlalchemy deals model"""

    __tablename__ = "bookcontents3"  # 테이블 이름

    #컬럼 데이터 타입 작성
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    img = Column(String(500))
    text = Column(String(10000))
    url = Column(String(500))
    description = Column(String(10000))

    # def __init__(self,title,img,text,url):
    #     self.title = title
    #     self.img = img
    #     self.text = text
    #     self.url = url
