import sqlite3

class DataProvider:
	def __init__(self):
		self.db = sqlite3.connect("local.db")
		self.initDB()

	def existsTable(self, tablename):
		res = self.db.execute("SELECT 1 FROM sqlite_master WHERE tbl_name = ?", (tablename,))
		if (res.fetchone()):
			return True
		return False

	def initDB(self):
		if (not self.existsTable("categories")):
			self.db.execute("CREATE TABLE 'categories' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT )")
		if (not self.existsTable("snipps")):
			self.db.execute("CREATE TABLE 'snipps' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT, 'code' TEXT )")

	def getCategories(self):
		ret = []
		for row in self.db.execute("SELECT id, name FROM categories ORDER BY name ASC"):
			ret.append([int(row[0]), row[1]])
		return ret

	def catAdd(self, text):
		self.db.execute("INSERT INTO categories (name) VALUES (?)", (text,))
		self.db.commit()

	def __del__(self):
		self.db.close()

