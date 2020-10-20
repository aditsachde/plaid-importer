from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.types import DECIMAL
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

Base = declarative_base()

class Items(Base):
    __tablename__ = "items"
    id = Column("id", Integer, primary_key=True, index=True)
    item_id = Column("item_id", String, nullable=False, unique=True)
    data = Column("data", JSONB, nullable=False)
    accounts = relationship("Accounts", back_populates="item")

class Accounts(Base):
    __tablename__ = "accounts"    
    
    id = Column("id", Integer, primary_key=True, index=True)
    item_id = Column("item_id", String, ForeignKey("items.item_id"), nullable=False)
    account_id = Column("account_id", String, nullable=False, unique=True)
    data = Column("data", JSONB, nullable=False)
    item = relationship("Items", back_populates="accounts")
    transactions = relationship("Transactions", back_populates="account")
    balances = relationship("Balances", back_populates="account")

class Transactions(Base):
    __tablename__ = "transactions"    
    
    id = Column("id", Integer, primary_key=True, index=True)
    account_id = Column("account_id", String, ForeignKey("accounts.account_id"), nullable=False)
    transaction_id = Column("transaction_id", String, nullable=False, unique=True)
    data = Column("data", JSONB, nullable=False)
    account = relationship("Accounts", back_populates="transactions")

class Balances(Base):
    __tablename__ = "balances"

    id = Column("id", Integer, primary_key=True, index=True)
    account_id = Column("account_id", String, ForeignKey("accounts.account_id"), nullable=False)
    available = Column("available", DECIMAL(precision=11, scale=2), nullable=True)
    current = Column("current", DECIMAL(precision=11, scale=2), nullable=False)
    limit = Column("limit", DECIMAL(precision=11, scale=2), nullable=True)
    currency = Column("currency", String, nullable=False)
    timestamp = Column("timestamp", DateTime, nullable=False)
    account = relationship("Accounts", back_populates="balances")