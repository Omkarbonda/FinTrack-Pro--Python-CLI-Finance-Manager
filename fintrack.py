import sys
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

# --- Configuration ---
DB_NAME = 'fintrack.db'
Base = declarative_base()

# --- Database Models ---

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

# --- Database Initialization ---
def init_db():
    engine = create_engine(f'sqlite:///{DB_NAME}')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

# --- Core Modules ---

def add_category(session):
    print("\n--- Add Category ---")
    name = input("Enter category name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    try:
        new_cat = Category(name=name)
        session.add(new_cat)
        session.commit()
        print(f"Success: Category '{name}' added.")
    except IntegrityError:
        session.rollback()
        print(f"Error: Category '{name}' already exists.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

def add_expense(session):
    print("\n--- Add Expense ---")
    categories = session.query(Category).all()
    if not categories:
        print("Error: No categories found. Add a category first.")
        return

    print("Available Categories:")
    for cat in categories:
        print(f"{cat.id}. {cat.name}")

    try:
        cat_id = int(input("Enter Category ID: "))
        if not session.query(Category).get(cat_id):
            print("Error: Invalid Category ID.")
            return

        title = input("Enter Expense Title: ").strip()
        amount = float(input("Enter Amount: "))
        date_str = input("Enter Date (YYYY-MM-DD) [Leave empty for today]: ").strip()
        
        if date_str:
            expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            expense_date = datetime.now().date()

        # Budget Check
        check_budget_alert(session, amount, expense_date)

        new_expense = Expense(title=title, amount=amount, date=expense_date, category_id=cat_id)
        session.add(new_expense)
        session.commit()
        print(f"Success: Expense '{title}' added.")
        
    except ValueError:
        print("Error: Invalid input format.")
    except Exception as e:
        print(f"Error: {e}")

def check_budget_alert(session, new_amount, date_obj):
    month_str = date_obj.strftime('%Y-%m')
    budget = session.query(Budget).filter_by(month=month_str).first()
    
    if budget:
        # Calculate total spending for this month
        start_date = date_obj.replace(day=1)
        # Simple query for month total
        total_spent = session.query(text("SUM(amount)")).select_from(Expense).filter(
            text(f"strftime('%Y-%m', date) = '{month_str}'")
        ).scalar() or 0.0
        
        if (total_spent + new_amount) > budget.limit_amount:
            print(f"\n[!!!] WARNING: This expense will exceed your budget of {budget.limit_amount} for {month_str}!")
            print(f"Current Spending: {total_spent}, New Total: {total_spent + new_amount}\n")

def set_budget(session):
    print("\n--- Set Monthly Budget ---")
    try:
        month_str = input("Enter Month (YYYY-MM): ").strip()
        # Validate format
        datetime.strptime(month_str, '%Y-%m')
        
        limit = float(input("Enter Budget Limit: "))
        
        # Check if exists
        existing = session.query(Budget).filter_by(month=month_str).first()
        if existing:
            print(f"Updating existing budget for {month_str} (Old: {existing.limit_amount})")
            existing.limit_amount = limit
        else:
            new_budget = Budget(month=month_str, limit_amount=limit)
            session.add(new_budget)
        
        session.commit()
        print(f"Success: Budget for {month_str} set to {limit}.")
    except ValueError:
        print("Error: Invalid format.")

def add_subscription(session):
    print("\n--- Add Subscription ---")
    try:
        name = input("Service Name: ").strip()
        amount = float(input("Monthly Amount: "))
        next_date_str = input("Next Due Date (YYYY-MM-DD): ").strip()
        next_date = datetime.strptime(next_date_str, '%Y-%m-%d').date()

        sub = Subscription(name=name, amount=amount, next_due_date=next_date)
        session.add(sub)
        session.commit()
        print(f"Success: Subscription '{name}' added.")
    except ValueError:
        print("Error: Invalid input.")

def search_expenses(session):
    print("\n--- Search Expenses by Date ---")
    date_str = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        # Using Raw SQL as per requirements logic demonstration (mixed usage)
        # But ORM is safer. Let's use ORM for consistency or Raw SQL if requested.
        # Requirement: "Find expenses by date using SQL query" -> Let's use Raw SQL
        
        sql = text("SELECT title, amount, category_id FROM expenses WHERE date = :d")
        result = session.execute(sql, {'d': target_date})
        
        print(f"\nExpenses on {date_str}:")
        found = False
        for row in result:
            found = True
            # Fetch category name separately or join (keeping it simple here)
            cat = session.query(Category).get(row[2])
            cat_name = cat.name if cat else "Unknown"
            print(f"- {row[0]} ({cat_name}): ${row[1]}")
            
        if not found:
            print("No records found.")
            
    except ValueError:
        print("Error: Invalid date format.")

def generate_report(session):
    print("\n--- Category-wise Spending Report (Raw SQL) ---")
    sql = text("""
        SELECT c.name, SUM(e.amount) as total
        FROM categories c
        JOIN expenses e ON c.id = e.category_id
        GROUP BY c.name
    """)
    
    try:
        result = session.execute(sql)
        print(f"{'Category':<20} | {'Total Amount':<15}")
        print("-" * 40)
        for row in result:
            print(f"{row[0]:<20} | ${row[1]:<15.2f}")
    except Exception as e:
        print(f"Error generating report: {e}")

# --- Main Menu ---

def main_menu():
    print("\n" + "="*40)
    print("      FINTRACK PRO - FINANCE MANAGER      ")
    print("="*40)
    print("1. Add Category")
    print("2. Add Expense")
    print("3. Set Monthly Budget")
    print("4. Add Subscription")
    print("5. Search Expenses (Date)")
    print("6. Generate Report (Category-wise)")
    print("7. Exit")
    print("="*40)

def main():
    session = init_db()
    print("System Initialized.")
    
    while True:
        main_menu()
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == '1':
            add_category(session)
        elif choice == '2':
            add_expense(session)
        elif choice == '3':
            set_budget(session)
        elif choice == '4':
            add_subscription(session)
        elif choice == '5':
            search_expenses(session)
        elif choice == '6':
            generate_report(session)
        elif choice == '7':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
