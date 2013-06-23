#!/usr/bin/python2

from gi.repository import Gtk

class HelloWorld:

	def destroy(self, widget, data=None):
		Gtk.main_quit()

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("layout.glade")
		self.window = builder.get_object("mainWindow")
		self.window.connect("delete-event", self.destroy)
		self.window.show()
		

	def main(self):
		Gtk.main()
	

if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()
