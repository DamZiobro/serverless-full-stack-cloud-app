import logging

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

#use dataclass from python 3.7+ in order to be possible to JSON serialise it
@dataclass
class Author(Base):
    __tablename__ = "author"

    author_id: int
    first_name: str
    last_name: str

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

@dataclass
class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("author.author_id"))
    author = relationship("Author", backref="books")

    def __repr__(self):
        return f"{self.title} by {self.author.first_name} {self.author.last_name}"


# Create Tables
def create_tables(engine):
    logging.info("****** Creating/Updating Tables ******")
    Base.metadata.create_all(bind=engine)
