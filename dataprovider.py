import sqlite3

class DataProvider:
	def __init__(self):
		self.db = sqlite3.connect("local.db")
		self.initDB()

	def tableExists(self, tablename):
		res = self.db.execute("SELECT 1 FROM sqlite_master WHERE tbl_name = ?", (tablename,))
		if (res.fetchone()):
			return True
		return False

	def initDB(self):
		if (not self.tableExists("categories")):
			self.db.execute("CREATE TABLE 'categories' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT )")
		if (not self.tableExists("snipps")):
			self.db.execute("CREATE TABLE 'snipps' ( 'id' INTEGER PRIMARY KEY, 'cat_id' INTEGER, 'name' TEXT, 'code' TEXT, 'lang' INTEGER )")
		if (not self.tableExists("langs")):
			self.db.execute("CREATE TABLE 'langs' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT )")
		if (not self.tableExists("tagnames")):
			self.db.execute("CREATE TABLE 'tagnames' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT )")
		if (not self.tableExists("tags")):
			self.db.execute("CREATE TABLE 'tags' ( 'id' INTEGER PRIMARY KEY, 'tag_id' INTEGER, 'snip_id' INTEGER )")

	def catGet(self):
		ret = []
		for row in self.db.execute("SELECT id, name FROM categories ORDER BY name ASC"):
			ret.append([int(row[0]), row[1]])
		return ret

	def snipGet(self, id):
		res = self.db.execute("SELECT snipps.id, snipps.name, code, langs.name FROM snipps LEFT JOIN langs on snipps.lang = langs.id WHERE snipps.id = ? LIMIT 1", (id,))
		row = res.fetchone()
		if not row is None:
			return (int(row[0]), row[1] or '', row[2] or '', row[3] or '', []) # id, name, code, lang, tags
		return None

	def snipSave(self, catid, id, name, code, lang, tags):
		res = self.db.execute("SELECT id FROM langs WHERE name = ?", (lang,))
		row = res.fetchone()
		if row:
			langid = row[0]
		else:
			res = self.db.execute("INSERT INTO langs (name) VALUES(?)", (lang,))
			langid = res.lastrowid

		if id is None:
			self.db.execute("INSERT INTO snipps (cat_id, name, code, lang) VALUES (?, ?, ?, ?)", (catid, name, code, langid))
		else:
			self.db.execute("UPDATE snipps SET name = ?, code = ?, lang = ? WHERE id = ?", (name, code, langid, id))
		self.db.commit()

	def dump(self, filename):
		with open(filename, 'w') as f:
		    for line in self.db.iterdump():
		        f.write('%s\n' % line)

	def snipDel(self, id):
		self.db.execute("DELETE FROM snipps WHERE id = ?", (id,))
		self.db.commit()

	def snipsOfCatDel(self, id):
		self.db.execute("DELETE FROM snipps WHERE cat_id = ?", (id,))
		self.db.commit()

	def entGet(self, id):
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

