import unittest
from finance.db import Database
from finance.auth import Auth
from finance.fin import Finance
import tempfile, os

class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.db = Database(self.tmp.name)
        self.auth = Auth(self.db)
        self.auth.register("user1", "pass")
        self.uid = self.auth.login("user1", "pass")
        self.fin = Finance(self.db, self.uid)

    def tearDown(self):
        self.db.close()
        os.unlink(self.tmp.name)

    def test_add_and_list_transaction(self):
        self.fin.add_transaction("income", "salary", 50000, "2025-10-01")
        self.fin.add_transaction("expense", "food", 1000, "2025-10-02")
        self.fin.list_transactions()

if __name__ == "__main__":
    unittest.main()
