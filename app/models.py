from sqlalchemy import Column,Integer,String,DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from .database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String, unique=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    created_date = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    updated_date = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc),nullable=False)
    profile_image = Column(String,nullable=False)
    
    # # Relationships
    # blogs = relationship("Blog", back_populates="author")  # One-to-many with Blog
    # comments = relationship("Comment", back_populates="user")  # One-to-many with Comment
    

class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    content = Column(Text,nullable=False)
    image = Column(String, nullable=False)
    created_date = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    updated_date = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc),nullable=False)
    author_id = Column(Integer,ForeignKey("user.id"),nullable=False,index=True)
    
    # # Relationships
    # author = relationship("User", back_populates="blogs")  # Many-to-one with User
    # comments = relationship("Comment", back_populates="blog")  # One-to-many with Comment

    

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer,primary_key=True,index=True)
    content = Column(Text,nullable=False)
    updated_date = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc),nullable=False)
    author_id = Column(Integer,ForeignKey("user.id"),nullable=False,index=True)
    blog_id = Column(Integer,ForeignKey('blog.id'),nullable=False,index=True)
    user_id = Column(Integer,ForeignKey('user.id'),nullable=False,index=True)
    
    # # Relationships
    # blog = relationship("Blog", back_populates="comments")  # Many-to-one with Blog
    # user = relationship("User", back_populates="comments")  # Many-to-one with User
    
    
    