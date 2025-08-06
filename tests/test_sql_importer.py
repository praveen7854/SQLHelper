import unittest
from components.sql_importer import SQLImporter

class TestSQLImporter(unittest.TestCase):
    def test_import_sql(self):
        db_config = {
            "user": "root",
            "password": "",
            "host": "localhost",
            "database": "test_db"
        }
        # Assuming a test.sql file exists in the directory with valid SQL
        returncode, stdout, stderr = SQLImporter.import_sql("test.sql", "test_table", db_config)
        self.assertEqual(returncode, 0)
        self.assertIn("Success", stdout)
