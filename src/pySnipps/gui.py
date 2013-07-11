# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:11:37 2013

@author: hans
"""


class Gui:
    @staticmethod
    def init(destroy, catPress, catSelChanged, catToggleAutoexpand, catNew, catDel, entSelChanged, snippsPress, snipNew, snipCopy, snipSave, snipDel):
        try:
            from gi.repository import Gtk, Gdk
            return GuiGtk(destroy, catPress, catSelChanged, catToggleAutoexpand, catNew, catDel, entSelChanged, snippsPress, snipNew, snipCopy, snipSave, snipDel)
        except ImportError:
            try:
                import PyQt4.QtCore as qt
                return GuiQT(destroy, catPress, catSelChanged, catToggleAutoexpand, catNew, catDel, entSelChanged, snippsPress, snipNew, snipCopy, snipSave, snipDel)
            except ImportError:
                return None

    def createMainWindow(self):
        pass
    def notify(self):
        pass
    def run(self):
        pass

class GuiQT(Gui):
    pass

class GuiGtk(Gui):
    def __init__(self, destroy, catPress, catSelChanged, catToggleAutoexpand, catNew, catDel, entSelChanged, snippsPress, snipNew, snipCopy, snipSave, snipDel):
        builder = Gtk.Builder()
        layoutpath=os.path.join(os.path.dirname(__file__), 'resources/layout.glade')
        builder.add_from_file(layoutpath)
        self.dlgCat = builder.get_object("dlgCat")
        self.dlgCatText = builder.get_object("dlgCatText")
        self.dlgCatPar = builder.get_object("dlgCatPar")
        self.dlgLsCatCombo = builder.get_object("dlgLsCatCombo")
        self.window = builder.get_object("mainWindow")
        self.window.connect("delete-event", destroy) # callback
        self.window.show()

        self.popup = builder.get_object("catPopup")
        actCatAutoexpand = builder.get_object("actCatAutoexpand")
        actCatAutoexpand.connect("activate", catToggleAutoexpand) # callback
        self.popAutoexpand = builder.get_object("popAutoexpand")

        self.tvCat = builder.get_object("tvCat")
        self.tvCat.connect("button-press-event", catPress) # callback
        self.tsCat = builder.get_object("tsCat")
        self.selCat = builder.get_object("selCat")
        self.selCat.connect("changed", catSelChanged) # callback
        actCatNew = builder.get_object("actCatNew")
        actCatNew.connect("activate", catNew) # callback
        actCatDel = builder.get_object("actCatDel")
        actCatDel.connect("activate", catDel) # callback

        self.selEnt = builder.get_object("selEnt")
        self.selEnt.connect("changed", entSelChanged) # callback
        self.snipName = builder.get_object("snipName")
        self.snipLang = builder.get_object("snipLang")
        self.snipTags = builder.get_object("snipTags")
        self.snipCode = builder.get_object("snipCode")

        self.tvSnipps = builder.get_object("tvSnipps")
        self.tvSnipps.connect("button-press-event", snippsPress) # callback
        self.lsSnipps = builder.get_object("lsSnipps")
        actSnipNew = builder.get_object("actSnipNew")
        actSnipNew.connect("activate", snipNew) # callback
        actSnipCopy = builder.get_object("actSnipCopy")
        actSnipCopy.connect("activate", snipCopy) # callback
        actSnipSave = builder.get_object("actSnipSave")
        actSnipSave.connect("activate", snipSave) # callback
        actSnipDel = builder.get_object("actSnipDelete")
        actSnipDel.connect("activate", snipDel) # callback

    def run(self):
        Gtk.main()

