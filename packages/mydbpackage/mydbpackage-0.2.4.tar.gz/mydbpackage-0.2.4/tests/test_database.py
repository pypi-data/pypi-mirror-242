# tests/test_database.py
import unittest
# from mypackage.database import MyDB
from mydbpackage.database import MyDB

test =['name','roll no','card no', 'class', 'section']
value = [['test','1','101', '10', 'A'],['test1','2','102', '10', 'A'],['test2','3','103', '10', 'A'],['test3','4','104', '10', 'A']]
class TestMyDB(unittest.TestCase):
    def test_create_table(self):
        db = MyDB("localhost", "root", "testpackage")
        db.create_table("schools",test)
        # Add assertions for table creation

    def test_insert_user(self):
        db = MyDB("localhost", "root", "testpackage")
        # db.create_table()
        db.insert_log(value,"schools")
        users = db.get_users()
        print(users)
        # Add assertions for user insertion

if __name__ == "__main__":
    unittest.main()
