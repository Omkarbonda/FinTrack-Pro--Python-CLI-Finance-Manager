from datetime import datetime
from sqlalchemy import text
from .models import Budget, Expense

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

def check_budget_alert(session, new_amount, date_obj):
    month_str = date_obj.strftime('%Y-%m')
    budget = session.query(Budget).filter_by(month=month_str).first()
    
    if budget:
        # Calculate total spending for this month
        total_spent = session.query(text("SUM(amount)")).select_from(Expense).filter(
            text(f"strftime('%Y-%m', date) = '{month_str}'")
        ).scalar() or 0.0
        
        if (total_spent + new_amount) > budget.limit_amount:
            print(f"\n[!!!] WARNING: This expense will exceed your budget of {budget.limit_amount} for {month_str}!")
            print(f"Current Spending: {total_spent}, New Total: {total_spent + new_amount}\n")
