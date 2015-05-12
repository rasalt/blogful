from sqlalchemy import String, Integer, DateTime, Text, Column
from .database import Base, session, engine
import datetime

class Post(Base):
  __tablename__ = "posts"
  id = Column(Integer, primary_key = True)
  title = Column(String(1024))
  content = Column(Text)
  datetime = Column(DateTime, default=datetime.datetime.now())
  
Base.metadata.create_all(engine)