#!/usr/bin/env python3
from finance.db import Database
from finance.auth import Auth
from finance.fin import Finance
import datetime, getpass, sys, os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    print("""
=============================
 PERSONAL FINANCE MANAGER
=============================
1. Register
2. Login
3. Exit
""")
    return input("Choose: ")

def user_menu():
    print("""
====================
  USER DASHBOARD
====================
1. Add transaction
2. List transactions
3. Update transaction
4. Delete transaction
5. Monthly report
6. Set budget
7. Check budget
8. Backup database
9. Logout
""")
    return input("Choose: ")

def main():
    db = Database()
    auth = Auth(db)

    while True:
        choice = main_menu().strip()
        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            auth.register(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            uid = auth.login(username, password)
            if uid:
                finance = Finance(db, uid)
                while True:
                    choice2 = user_menu().strip()
                    if choice2 == '1':
                        t_type = input("Type (income/expense): ")
                        category = input("Category: ")
                        amount = float(input("Amount: "))
                        date = input("Date (YYYY-MM-DD) [default=today]: ") or str(datetime.date.today())
                        desc = input("Description: ")
                        finance.add_transaction(t_type, category, amount, date, desc)
                    elif choice2 == '2':
                        finance.list_transactions()
                    elif choice2 == '3':
                        trans_id = int(input("Transaction ID: "))
                        amount = float(input("New amount: "))
                        finance.update_transaction(trans_id, amount)
                    elif choice2 == '4':
                        trans_id = int(input("Transaction ID to delete: "))
                        finance.delete_transaction(trans_id)
                    elif choice2 == '5':
                        m = int(input("Month (1-12): "))
                        y = int(input("Year: "))
                        finance.monthly_report(m, y)
                    elif choice2 == '6':
                        m = int(input("Month (1-12): "))
                        y = int(input("Year: "))
                        amount = float(input("Budget amount: "))
                        finance.set_budget(m, y, amount)
                    elif choice2 == '7':
                        m = int(input("Month (1-12): "))
                        y = int(input("Year: "))
                        finance.check_budget(m, y)
                    elif choice2 == '8':
                        db.backup()
                    elif choice2 == '9':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            print("Goodbye 👋")
            db.close()
            sys.exit(0)
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()

