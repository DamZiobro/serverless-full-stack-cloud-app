import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Author(Base):
    __tablename__ = "author"

    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("author.author_id"))
    author = relationship("Author", backref="books")


# Create Tables
def create_tables(engine):
    logging.info("****** Creating/Updating Tables ******")
    Base.metadata.create_all(bind=engine)
