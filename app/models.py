from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    expenses = relationship("Expense", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, default=datetime.now().date)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    category = relationship("Category", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(title='{self.title}', amount={self.amount})>"

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    next_due_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Subscription(name='{self.name}', amount={self.amount})>"

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False) # Format: YYYY-MM
    limit_amount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Budget(month='{self.month}', limit={self.limit_amount})>"
