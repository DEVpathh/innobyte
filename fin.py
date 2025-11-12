import datetime

class Finance:
    def __init__(self, db, user_id: int):
        self.db = db
        self.user_id = user_id

    def add_transaction(self, t_type: str, category: str, amount: float, date: str, description: str = ""):
        cur = self.db.conn.cursor()
        cur.execute("""
            INSERT INTO transactions (user_id, type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.user_id, t_type, category, amount, date, description))
        self.db.conn.commit()
        print("✅ Transaction added.")

    def update_transaction(self, trans_id: int, amount: float):
        cur = self.db.conn.cursor()
        cur.execute("""
            UPDATE transactions SET amount=? WHERE id=? AND user_id=?
        """, (amount, trans_id, self.user_id))
        self.db.conn.commit()
        print("✅ Transaction updated.")

    def delete_transaction(self, trans_id: int):
        cur = self.db.conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (trans_id, self.user_id))
        self.db.conn.commit()
        print("✅ Transaction deleted.")

    def list_transactions(self):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY date DESC", (self.user_id,))
        rows = cur.fetchall()
        if not rows:
            print("No transactions yet.")
            return
        for r in rows:
            print(f"{r['id']:3d} | {r['date']} | {r['type']:<7} | {r['category']:<10} | ₹{r['amount']:>8.2f} | {r['description']}")

    def monthly_report(self, month: int, year: int):
        cur = self.db.conn.cursor()
        cur.execute("""
            SELECT type, SUM(amount) as total FROM transactions
            WHERE user_id=? AND strftime('%m', date)=? AND strftime('%Y', date)=?
            GROUP BY type
        """, (self.user_id, f"{month:02d}", str(year)))
        totals = {r["type"]: r["total"] for r in cur.fetchall()}
        income = totals.get("income", 0)
        expense = totals.get("expense", 0)
        balance = income - expense
        print(f"\n📅 {month:02d}/{year}")
        print(f"   Income:  ₹{income:.2f}")
        print(f"   Expense: ₹{expense:.2f}")
        print(f"   Balance: ₹{balance:.2f}")

    def set_budget(self, month: int, year: int, amount: float):
        cur = self.db.conn.cursor()
        cur.execute("""
            INSERT INTO budgets (user_id, month, year, amount)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, month, year) DO UPDATE SET amount=excluded.amount
        """, (self.user_id, month, year, amount))
        self.db.conn.commit()
        print("✅ Budget set successfully.")

    def check_budget(self, month: int, year: int):
        cur = self.db.conn.cursor()
        cur.execute("""
            SELECT amount FROM budgets WHERE user_id=? AND month=? AND year=?
        """, (self.user_id, month, year))
        b = cur.fetchone()
        if not b:
            print("No budget set.")
            return
        budget = b["amount"]
        cur.execute("""
            SELECT SUM(amount) as spent FROM transactions
            WHERE user_id=? AND type='expense'
            AND strftime('%m', date)=? AND strftime('%Y', date)=?
        """, (self.user_id, f"{month:02d}", str(year)))
        spent = cur.fetchone()["spent"] or 0
        print(f"Budget: ₹{budget:.2f}, Spent: ₹{spent:.2f}, Remaining: ₹{budget - spent:.2f}")
