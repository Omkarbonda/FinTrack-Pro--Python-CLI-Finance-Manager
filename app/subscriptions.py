from datetime import datetime
from .models import Subscription

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
