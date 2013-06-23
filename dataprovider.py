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
			self.db.execute("CREATE TABLE 'snipps' ( 'id' INTEGER PRIMARY KEY, 'cat_id' INTEGER, 'name' TEXT, 'code' TEXT )")

	def getCategories(self):
		ret = []
		for row in self.db.execute("SELECT id, name FROM categories ORDER BY name ASC"):
			ret.append([int(row[0]), row[1]])
		return ret

	def snipGet(self, id):
		res = self.db.execute("SELECT id, name, code FROM snipps WHERE id = ? LIMIT 1", (id,))
		row = res.fetchone()
		if not row is None:
			return [int(row[0]), row[1], row[2]]
		return None

	def snipSave(self, catid, id, name, text):
		if id is None:
			self.db.execute("INSERT INTO snipps (cat_id, name, code) VALUES (?, ?, ?)", (catid, name, text))
		else:
			self.db.execute("UPDATE snipps SET name = ?, code = ? WHERE id = ?", (name, text, id))
		self.db.commit()

	def snipDel(self, id):
		self.db.execute("DELETE FROM snipps WHERE id = ?", (id,))
		self.db.commit()

	def snipsOfCatDel(self, id):
		self.db.execute("DELETE FROM snipps WHERE cat_id = ?", (id,))
		self.db.commit()

	def getEntries(self, id):
		ret = []
		for row in self.db.execute("SELECT id, name FROM snipps WHERE cat_id = ? ORDER BY name ASC", (id,)):
			ret.append([int(row[0]), row[1]])
		return ret

	def catAdd(self, text):
		self.db.execute("INSERT INTO categories (name) VALUES (?)", (text,))
		self.db.commit()

	def catDel(self, id):
		self.db.execute("DELETE FROM categories WHERE id = ?", (id,))
		self.db.commit()
		self.snipsOfCatDel(id)

	def __del__(self):
		self.db.close()

