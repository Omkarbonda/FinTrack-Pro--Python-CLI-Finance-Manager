import sys
from app.database import init_db
from app.expense import add_category, add_expense
from app.budget import set_budget
from app.subscriptions import add_subscription
from app.search import search_expenses
from app.reports import generate_report

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
