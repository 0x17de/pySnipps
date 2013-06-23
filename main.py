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

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("layout.glade")
		self.window = builder.get_object("mainWindow")
		actSnipNew = builder.get_object("actSnipNew")
		actSnipNew.connect("activate", self.snipNew)
		self.window.connect("delete-event", self.destroy)
		self.window.show()

		self.db = DataProvider()
		self.db.showCategories()
		

	def main(self):
		Gtk.main()
	

if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()
