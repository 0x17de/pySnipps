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
			self.db.execute("CREATE TABLE 'categories' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT, 'parent' INTEGER )")
		if (not self.tableExists("snipps")):
			self.db.execute("CREATE TABLE 'snipps' ( 'id' INTEGER PRIMARY KEY, 'cat_id' INTEGER, 'name' TEXT, 'code' TEXT, 'lang' INTEGER )")
		if (not self.tableExists("langs")):
			self.db.execute("CREATE TABLE 'langs' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT )")
		if (not self.tableExists("tagnames")):
			self.db.execute("CREATE TABLE 'tagnames' ( 'id' INTEGER PRIMARY KEY, 'name' TEXT )")
		if (not self.tableExists("tags")):
			self.db.execute("CREATE TABLE 'tags' ( 'id' INTEGER PRIMARY KEY, 'tag_id' INTEGER, 'snip_id' INTEGER )")

	def catGet(self, parent=0):
		ret = []
		for row in self.db.execute("SELECT id, name FROM categories WHERE parent = ? ORDER BY name ASC", (parent,)):
			ret.append([int(row[0]), row[1]])
		return ret

	def snipTagsGet(self, id, bAsString = False):
		dbtagids = []
		if bAsString:
			for tagrow in self.db.execute("SELECT name FROM tags LEFT JOIN tagnames ON tagnames.id = tag_id WHERE snip_id = ?", (id,)):
				dbtagids.append(tagrow[0])
		else:
			for tagrow in self.db.execute("SELECT id FROM tags WHERE snip_id = ?", (id,)):
				dbtagids.append(tagrow[0])
		return dbtagids

	def snipGet(self, id):
		res = self.db.execute("SELECT snipps.id, snipps.name, code, langs.name FROM snipps LEFT JOIN langs on snipps.lang = langs.id WHERE snipps.id = ? LIMIT 1", (id,))
		row = res.fetchone()
		tags = self.snipTagsGet(id, True)
		if not row is None:
			return (int(row[0]), row[1] or '', row[2] or '', row[3] or '', tags) # id, name, code, lang, tags
		return None

	def snipSaveLang(self, lang):
		res = self.db.execute("SELECT id FROM langs WHERE name = ?", (lang,))
		row = res.fetchone()
		if row:
			langid = row[0]
		else:
			res = self.db.execute("INSERT INTO langs (name) VALUES(?)", (lang,))
			langid = res.lastrowid
		return langid

	def snipSaveGetAllTags(self, id, tags):
		dbtagids = self.snipTagsGet(id)

		tagids = []
		for tagname in tags:
			res = self.db.execute("SELECT id FROM tagnames WHERE name = ?", (tagname,))
			row = res.fetchone()
			if row:
				tagid = row[0]
			else:
				newrow = self.db.execute("INSERT INTO tagnames (name) VALUES (?)", (tagname,))
				tagid = newrow.lastrowid
				
			tagids.append(tagid)

		return (tagids, dbtagids)

	def snipSave(self, catid, id, name, code, lang, tags):
		langid = self.snipSaveLang(lang)

		if id is None:
			row = self.db.execute("INSERT INTO snipps (cat_id, name, code, lang) VALUES (?, ?, ?, ?)", (catid, name, code, langid))
			id = row.lastrowid
		else:
			self.db.execute("UPDATE snipps SET name = ?, code = ?, lang = ? WHERE id = ?", (name, code, langid, id))

		(tagids, dbtagids) = self.snipSaveGetAllTags(id, tags)

		for tagid in tagids:
			if not tagid in dbtagids:
				self.db.execute("INSERT INTO tags (tag_id, snip_id) VALUES (?, ?)", (tagid, id))

		for tagid in dbtagids:
			if not tagid in tagids:
				self.db.execute("DELETE FROM tags WHERE tag_id = ? AND snip_id = ?", (tagid,id))

		self.db.commit()

	def dump(self, filename):
		with open(filename, 'w') as f:
		    for line in self.db.iterdump():
		        f.write('%s\n' % line)

	def snipDel(self, id, bCommitDB = True):
		self.db.execute("DELETE FROM snipps WHERE id = ?", (id,))
		self.db.execute("DELETE FROM tags WHERE snip_id = ?", (id,))
		if bCommitDB:
			self.db.commit()

	def snipsOfCatDel(self, id, bCommitDB = True):
		for cat in self.db.execute("SELECT id FROM snipps WHERE cat_id = ?", (id,)):
			self.snipDel(cat[0], False)
		if bCommitDB:
			self.db.commit()

	def entGet(self, id):
		ret = []
		for row in self.db.execute("SELECT id, name FROM snipps WHERE cat_id = ? ORDER BY name ASC", (id,)):
			ret.append([int(row[0]), row[1]])
		return ret

	def catAdd(self, text):
		self.db.execute("INSERT INTO categories (name, parent) VALUES (?, '0')", (text,))
		self.db.commit()

	def catDel(self, id, bCommitDB = True):
		for cat in self.db.execute("SELECT id FROM categories WHERE parent = ?", (id,)):
			catDel(selof, id, False)

		self.db.execute("DELETE FROM categories WHERE id = ?", (id,))
		self.snipsOfCatDel(id, False)
		if bCommitDB:
			self.db.commit()

	def __del__(self):
		self.db.close()

