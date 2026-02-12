# FinTrack Pro - CLI Finance Manager

## Project Structure
```
FinTrack-Pro/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── expense.py
│   ├── budget.py
│   ├── reports.py
│   ├── subscriptions.py
│   └── search.py
│
├── fintrack.py
├── requirements.txt
├── .gitignore
├── README.md
└── fintrack.db
```


## Introduction
FinTrack Pro is a command-line based personal finance management system tailored for tracking daily expenses, managing subscriptions, and monitoring monthly budgets. Built with Python and SQLAlchemy, it offers a robust solution for personal finance tracking with a focus on ease of use and data persistence.

## Features
- **Expense Tracking**: Add, categorize, and view daily expenses.
- **Budget Management**: Set monthly budgets and get alerts when approaching or exceeding limits.
- **Subscriptions**: Keep track of recurring payments.
- **Analytics**: View category-wise spending reports using raw SQL queries.
- **Search**: Find expenses by specific dates.

## Technology Stack
- **Language**: Python 3.x
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Interface**: Command Line Interface (CLI)

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install sqlalchemy
   ```

## Usage

Run the application using Python:
```bash
python fintrack.py
```

### Menu Options
1. **Add Category**: Define improved categories for your expenses (e.g., Food, Travel, Bills).
2. **Add Expense**: Log a new expense under a category.
3. **Set Monthly Budget**: Define a spending limit for a specific month (YYYY-MM).
4. **Add Subscription**: Track recurring costs like Netflix or Gym.
5. **Search Expenses**: View all transactions for a specific date.
6. **Generate Report**: See a summary of spending per category.

## Database Schema
- **Categories**: `id`, `name`
- **Expenses**: `id`, `title`, `amount`, `date`, `category_id`
- **Subscriptions**: `id`, `name`, `amount`, `next_due_date`
- **Budgets**: `id`, `month`, `limit_amount`

## Future Enhancements
- Export data to CSV/Excel.
- Graphical User Interface (GUI) or Web Dashboard.
- User Authentication.

---
*Developed for Resume Showcase & Interview Demonstration.*
