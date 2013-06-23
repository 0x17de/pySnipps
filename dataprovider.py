import sqlite3

class DataProvider:
	def __init__(self):
		self.db = sqlite3.connect("local.db")
		self.initDB()

	def existsTable(self, tablename):
		res = self.db.execute("SELECT 1 FROM sqlite_master WHERE tbl_name = '%s'" % tablename)
		if (res.fetchone()):
			return True
		return False

	def initDB(self):
		if (not self.existsTable("categories")):
			self.db.execute("CREATE TABLE 'categories' ( 'id' INTEGER NOT NULL, 'name' TEXT )")
		if (not self.existsTable("snipps")):
			self.db.execute("CREATE TABLE 'snipps' ( 'id' INTEGER NOT NULL, 'name' TEXT, 'code' TEXT )")

	def showCategories(self):
		for row in self.db.execute("SELECT id, name FROM categories ORDER BY name ASC"):
			print row


	def __del__(self):
		self.db.close()

