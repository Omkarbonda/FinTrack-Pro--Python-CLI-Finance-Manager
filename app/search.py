from datetime import datetime
from sqlalchemy import text
from .models import Category

def search_expenses(session):
    print("\n--- Search Expenses by Date ---")
    date_str = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        sql = text("SELECT title, amount, category_id FROM expenses WHERE date = :d")
        result = session.execute(sql, {'d': target_date})
        
        print(f"\nExpenses on {date_str}:")
        found = False
        for row in result:
            found = True
            cat = session.query(Category).get(row[2])
            cat_name = cat.name if cat else "Unknown"
            print(f"- {row[0]} ({cat_name}): ${row[1]}")
            
        if not found:
            print("No records found.")
            
    except ValueError:
        print("Error: Invalid date format.")
