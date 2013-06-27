#!/usr/bin/python2

import sys
from gi.repository import Gtk, Gdk
from dataprovider import *

class SnippsGUI:

	def destroy(self, widget, data=None):
		Gtk.main_quit()

	def notify(self, text):
		dlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, text)
		dlg.run()
		dlg.destroy()

	def snipNew(self, widget, data=None):
		self.selEnt.unselect_all()
		self.entSelChanged()

	def catNew(self, widget):
		self.dlgCatPar.set_active(0)
		res = self.dlgCat.run()
		self.dlgCat.hide()
		text = self.dlgCatText.get_text()
		self.dlgCatText.set_text("")
		if res == 0:
			cbiter = self.dlgCatPar.get_active_iter()
			parid = self.dlgLsCatCombo.get(cbiter, 0)[0]
			self.db.catAdd(text, parid)
			self.refreshCategories()
			self.catSelChanged()

	def catDel(self, widget):
		(model, iter) = self.selCat.get_selected()
		if iter is None:
			return
		id = model.get_value(iter, 0)
		text = model.get_value(iter, 1)
		dlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "Delete '%s'?" % text)
		res = dlg.run()
		dlg.destroy()
		if res == Gtk.ResponseType.YES:
			self.db.catDel(id)
			self.refreshCategories()

	def snipCopy(self, widget=None):
		buf = self.snipCode.get_buffer()
		clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		clip.set_text(buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True), -1)

	def refreshSnipp(self):
		snip = self.db.snipGet(self.selEntID)
		if snip is None:
			self.snipName.set_text("")
			self.snipCode.get_buffer().set_text("")
			self.snipLang.set_text("")
			self.snipTags.set_text("")
		else:
			self.snipName.set_text(snip[1])
			self.snipCode.get_buffer().set_text(snip[2])
			self.snipLang.set_text(snip[3])
			self.snipTags.set_text(", ".join(snip[4]))

	def trimarr(self, arr):
		res = []
		for text in arr:
			res.append(text.strip())
		return res

	def snipSave(self, widget=None):
		if not self.selCatID is None:
			buf = self.snipCode.get_buffer()
			code = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
			tags = self.trimarr(self.snipTags.get_text().split(","))
			if not tags is None and tags[0] == '':
				tags = []
			self.db.snipSave(self.selCatID, self.selEntID, self.snipName.get_text(), code, self.snipLang.get_text(), tags)
			self.refreshEntries()

	def snipDel(self, widget=None):
		(model, iter) = self.selEnt.get_selected()
		if iter is None:
			return
		id = model.get_value(iter, 0)
		text = model.get_value(iter, 1)
		dlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "Delete '%s'?" % text)
		res = dlg.run()
		dlg.destroy()
		if res == Gtk.ResponseType.YES:
			self.db.snipDel(self.selEntID)
			self.refreshEntries()

	def refreshEntries(self):
		ent = self.db.entGet(self.selCatID)
		self.lsSnipps.clear()
		if not self.selCatID is None:
			for e in ent:
				self.lsSnipps.append(e)
		self.entSelChanged()

	def entSelChanged(self, widget=None):
		(model, iter) = self.selEnt.get_selected()
		if iter is None:
			self.selEntID = None
		else:
			self.selEntID = model.get_value(iter, 0)
		self.refreshSnipp()

	def refreshCategories(self, parentid=0, parentnode=None):
		if parentid == 0:
			self.tsCat.clear()
			self.dlgLsCatCombo.clear()
			self.dlgLsCatCombo.append([0, "--- Root ---"])
		for c in self.db.catGet(parentid):
			node = self.tsCat.append(parentnode, c[0:2])
			self.dlgLsCatCombo.append(c[0:2])
			self.refreshCategories(c[0], node)
			if int(c[2]) == 1:
				self.tvCat.expand_row(self.tsCat.get_path(node), False)
		if parentid == 0:
			self.catSelChanged()

	def catSelChanged(self, widget=None):
		(model, iter) = self.selCat.get_selected()
		if iter is None:
			self.selCatID = None
			self.snipName.set_sensitive(False)
			self.snipLang.set_sensitive(False)
			self.snipTags.set_sensitive(False)
			self.snipCode.set_sensitive(False)
		else:
			self.selCatID = model.get_value(iter, 0)
			self.snipName.set_sensitive(True)
			self.snipLang.set_sensitive(True)
			self.snipTags.set_sensitive(True)
			self.snipCode.set_sensitive(True)
		self.refreshEntries()

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("layout.glade")
		self.dlgCat = builder.get_object("dlgCat")
		self.dlgCatText = builder.get_object("dlgCatText")
		self.dlgCatPar = builder.get_object("dlgCatPar")
		self.dlgLsCatCombo = builder.get_object("dlgLsCatCombo")
		self.window = builder.get_object("mainWindow")
		self.window.connect("delete-event", self.destroy)
		self.window.show()

		self.db = DataProvider()

		self.tvCat = builder.get_object("tvCat")
		self.tsCat = builder.get_object("tsCat")
		self.selCat = builder.get_object("selCat")
		self.selCat.connect("changed", self.catSelChanged)
		actCatNew = builder.get_object("actCatNew")
		actCatNew.connect("activate", self.catNew)
		actCatDel = builder.get_object("actCatDel")
		actCatDel.connect("activate", self.catDel)

		self.selEnt = builder.get_object("selEnt")
		self.selEnt.connect("changed", self.entSelChanged)
		self.snipName = builder.get_object("snipName")
		self.snipLang = builder.get_object("snipLang")
		self.snipTags = builder.get_object("snipTags")
		self.snipCode = builder.get_object("snipCode")

		self.lsSnipps = builder.get_object("lsSnipps")
		actSnipNew = builder.get_object("actSnipNew")
		actSnipNew.connect("activate", self.snipNew)
		actSnipCopy = builder.get_object("actSnipCopy")
		actSnipCopy.connect("activate", self.snipCopy)
		actSnipSave = builder.get_object("actSnipSave")
		actSnipSave.connect("activate", self.snipSave)
		actSnipDel = builder.get_object("actSnipDelete")
		actSnipDel.connect("activate", self.snipDel)

		self.refreshCategories()
		self.catSelChanged()
		self.refreshEntries()

	def main(self):
		Gtk.main()
	

if __name__ == "__main__":
	if len(sys.argv) >= 3:
		if sys.argv[1] == 'dump':
			db = DataProvider()
			db.dump(sys.argv[2])
	else:
		w = SnippsGUI()
		w.main()

