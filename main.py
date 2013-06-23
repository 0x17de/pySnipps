#!/usr/bin/python2

from gi.repository import Gtk
from dataprovider import *

class HelloWorld:

	def destroy(self, widget, data=None):
		Gtk.main_quit()

	def notify(self, text):
		dlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, text)
		dlg.run()
		dlg.destroy()

	def snipNew(self, widget, data=None):
		self.notify("Not yet!")

	def catNew(self, widget):
		res = self.dlgCat.run()
		self.dlgCat.hide()
		text = self.dlgCatText.get_text()
		self.dlgCatText.set_text("")
		if res == 0:
			self.db.catAdd(text)
			self.refreshCategories()

	def catDel(self, widget):
		(model, iter) = self.selCat.get_selected()
		id = model.get_value(iter, 0)
		text = model.get_value(iter, 1)
		dlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "Delete '%s'?" % text)
		res = dlg.run()
		dlg.destroy()
		if res == Gtk.ResponseType.YES:
			self.db.catDel(id)
			self.refreshCategories()

	def refreshCategories(self):
		cat = self.db.getCategories()
		self.lsCat.clear()
		for c in cat:
			self.lsCat.append(c)

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("layout.glade")
		builder.add_from_file("newcat.glade")
		self.dlgCat = builder.get_object("dlgCat")
		self.dlgCatText = builder.get_object("dlgCatText")
		self.window = builder.get_object("mainWindow")
		self.window.connect("delete-event", self.destroy)
		self.window.show()

		self.db = DataProvider()

		self.lsCat = builder.get_object("lsCat")
		self.selCat = builder.get_object("selCat")
		actCatNew = builder.get_object("actCatNew")
		actCatNew.connect("activate", self.catNew)
		actCatDel = builder.get_object("actCatDel")
		actCatDel.connect("activate", self.catDel)

		self.lsSnippet = builder.get_object("lsSnipps")
		actSnipNew = builder.get_object("actSnipNew")
		actSnipNew.connect("activate", self.snipNew)

		self.refreshCategories()

		

	def main(self):
		Gtk.main()
	

if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()
