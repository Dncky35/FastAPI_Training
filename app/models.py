import sqlalchemy as sa
from .database import Base
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = "accounts"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, server_default=sa.text('now()'), nullable=False)

class Post(Base):
    __tablename__ = "posts"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    published = sa.Column(sa.Boolean, server_default='TRUE' ,nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, server_default=sa.text('now()'), nullable=False)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)

    owner = relationship("Account")

class Vote(Base):
    __tablename__ = "votes"
    
    account_id = sa.Column(sa.Integer, sa.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id = sa.Column(sa.Integer, sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    