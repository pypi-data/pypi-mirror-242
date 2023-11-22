# tests/test_database.py
import unittest
# from mypackage.database import MyDB
from my_package.database import MyDB

class TestMyDB(unittest.TestCase):
    def test_create_table(self):
        db = MyDB("localhost", "root", "testpackage")
        db.create_table("test")
        # Add assertions for table creation

    def test_insert_user(self):
        db = MyDB("localhost", "root", "testpackage")
        db.create_table()
        db.insert_log("http://127.0.0.1:8000/feed/",200)
        users = db.get_users()
        print(users)
        # Add assertions for user insertion

if __name__ == "__main__":
    unittest.main()
