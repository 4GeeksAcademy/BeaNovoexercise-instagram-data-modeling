import os
import sys
import enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, String, ForeignKey, Integer, Enum, Column, Table
from eralchemy2 import render_er
from typing import List

Base = declarative_base()

followers_table = Table(
    "followers",
    Base.metadata,
    Column("user_from_id", ForeignKey("user.id")),
    Column("user_to_id", ForeignKey("user.id")),
)

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=False)
    comments: Mapped[List["Comments"]] = relationship(back_populates="author")
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    following: Mapped[List["User"]] = relationship(
        "User",
        secondary=followers_table,
        primaryjoin=(id == followers_table.c.user_from_id),
        secondaryjoin=(id == followers_table.c.user_to_id),
        back_populates="followers"
    )
    
    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary=followers_table,
        primaryjoin=(id == followers_table.c.user_to_id),
        secondaryjoin=(id == followers_table.c.user_from_id),
        back_populates="following"
    )





class Comments(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    posts_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)
    # : Mapped["Post"] = relationship(back_populates="comments")



class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    # media: Mapped[int] = mapped_column(ForeignKey('media.id'), nullable=False)
    # comments: Mapped[List["Comments"]] = relationship(back_populates="posts")


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column(nullable=True)
    url: Mapped["User"] = relationship(back_populates="posts")
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)
    # comments: Mapped[List["Comments"]] = relationship(back_populates="posts")


    # comments: Mapped[List["Comments"]] = relationship(back_populates="posts")
    

# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id: Mapped[int] = mapped_column(primary_key=True)
#     post_id: Mapped[str] = mapped_column(nullable=False)

def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
