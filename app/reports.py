from sqlalchemy import text

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
