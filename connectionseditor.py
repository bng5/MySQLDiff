#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

#import _mysql
import gobject

import sys
from os import path#, environ
#import persistence
from persistence import *

__author__="Pablo Bangueses"


class ConnectionsEditor:

    def __init__(self):
        # TODO Remove
        if sys.platform == 'darwin':
            from AppKit import NSSearchPathForDirectoriesInDomains
            # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
            # NSApplicationSupportDirectory = 14
            # NSUserDomainMask = 1
            # True for expanding the tilde into a fully qualified path
            self.appdata = path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], 'bng5', 'mysqldiff')
        elif sys.platform == 'win32':
            self.appdata = path.join(environ['APPDATA'], 'bng5', 'mysqldiff')
        else:
            self.appdata = path.expanduser(path.join("~", '.bng5', 'mysqldiff'))
        # TODO Remove

        self.builder = gtk.Builder()
        self.builder.add_from_file("glade/connections_editor.ui")
        self.window = self.builder.get_object('window')
        self.builder.connect_signals(self)
        self.window.show_all()
        self.entry = {}
        self.entry_name = self.builder.get_object('name_entry')
        self.entry_name.connect('changed', self.changed_name_entry);
        self.entry['username'] = self.builder.get_object('username_entry')
        self.entry['username'].connect('changed', self.changed_entry, 'username')
        self.entry['pass'] = self.builder.get_object('pass_entry')
        self.entry['pass'].connect('changed', self.changed_entry, 'pass')
        self.entry['host'] = self.builder.get_object('host_entry')
        self.entry['host'].connect('changed', self.changed_entry, 'host')
        self.entry['port'] = self.builder.get_object('port_entry')
        self.entry['port'].connect('changed', self.changed_entry, 'port')
        self.entry['schema'] = self.builder.get_object('schema_entry')
        self.entry['schema'].connect('changed', self.changed_entry, 'schema')
        
        self.treeview = self.builder.get_object('storedConnections')
        self.model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
        self.treeview.set_model(self.model)
        render = gtk.CellRendererText() # renderer para la primera columna
        columna = gtk.TreeViewColumn("Connection Name", render, text=0) # primera columna de datos
        self.treeview.append_column(columna)
        self.bm = Bookmarks.Bookmarks(self.appdata)
        i = 0
        bookmarks = self.bm.getBookmarks()
        for sec in bookmarks:
            iterador = self.model.append()
            self.model.set_value(iterador, 0, sec)
            self.model.set_value(iterador, 1, bookmarks[sec])
            i = i + 1
        selection = self.treeview.get_selection()
        #selection.set_mode(gtk.selection)
        selection.connect('changed', self.demo_selected);

    def demo_selected(self, selection):
        model, iter = selection.get_selected()
        self.entry_name.set_text(model.get_value(iter, 0))
        fields = model.get_value(iter, 1)
        for entry in self.entry:
            self.entry[entry].set_text(fields[entry])

    def remove(self, widget):
        model, iter = self.treeview.get_selection().get_selected()
        if iter != None:
            model.remove(iter)

    def quit(self, widget):
        self.window.destroy()

    def apply(self, widget):
        save = True
        if self.bm.hash != self.bm.md5File():
            save = self.confirm('Las conexiones han cambiado desde que abrió esta ventana. ¿Desea remplazarlas?')
        if save == True:
            self.bm.save(self.model)
            self.quit(None)

    def confirm(self, message, title = 'Confirm'):
        dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL,
            message)
        dialog.set_title(title)
        response = dialog.run()
        dialog.destroy()
        return (response == gtk.RESPONSE_OK)

    def createEmpty(self, widget):
        name = 'New Connection'
        if hasattr(self, 'k'):
            self.k = self.k + 1
            name += ' '+str(self.k)
        else:
            self.k = 0
        iterador = self.model.append()
        self.model.set_value(iterador, 0, name)
        self.model.set_value(iterador, 1, {'username':'', 'pass': '', 'host': '', 'port': '3306', 'schema': ''})

    def mainQuit(self, widget):
        self.window.destroy()

    def changed_name_entry(self, widget):
        model, iter = self.treeview.get_selection().get_selected()
        model.set_value(iter, 0, widget.get_text())

    def changed_entry(self, widget, field = None):
        model, iter = self.treeview.get_selection().get_selected()
        data = model.get_value(iter, 1)
        data[field] = widget.get_text()
        model.set_value(iter, 1, data)
        #        for i in dir(widget):
        #            print i, getattr(widget, i)

if __name__ == "__main__":
    window = ConnectionsEditor()
    window.window.connect('destroy', gtk.main_quit)
    gtk.main()
    
