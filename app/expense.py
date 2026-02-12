from datetime import datetime
from sqlalchemy.exc import IntegrityError
from .models import Category, Expense
from .budget import check_budget_alert

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
