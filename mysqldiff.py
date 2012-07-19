#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import sys
from os import path#, environ
import _mysql
import connectionseditor
import ConnectDialog

import gobject

#import persistence
from persistence import *

import webbrowser



__author__="Pablo Bangueses"

url = {
    'help': 'http://bng5.net/help',
    'reportbug': 'http://bng5.net/bugs',
    'translate': 'http://bng5.net/translate'
}

class MysqlDiff:

    def __init__(self):

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
        ud = UserData.UserData(self.appdata)
        bm = Bookmarks.Bookmarks(self.appdata)
        #print bm.getBookmarks()

        self.builder = gtk.Builder()
        self.builder.add_from_file("glade/main_window.ui")
        self.window = self.builder.get_object('window')
        #self.builder.connect_signals(self)
        self.window.show_all()

        self.side = {}
        self.side[1] = {
            'button': self.builder.get_object('connect1'),
            'label': self.builder.get_object("connection1_label"),
            'db': None
        }
        self.side[2] = {
            'button': self.builder.get_object('connect2'),
            'label': self.builder.get_object("connection2_label"),
            'db': None
        }

        self.window.connect('destroy', self.mainQuit)
        self.builder.get_object('menu_file_quit').connect('activate', self.mainQuit)

        #self.conn1.button.connect('clicked', self.showConnectDialog, 1)
        self.side[1]['button'].connect('clicked', self.toggleConnection, self.side[1])
        self.side[2]['button'].connect('clicked', self.toggleConnection, self.side[2])

        self.connectimage1 = self.builder.get_object('connectimage1')
        self.connectimage2 = self.builder.get_object('connectimage2')
        
        # Menu
        menu_help_help = self.builder.get_object('menu_help_help')
        menu_help_help.connect('activate', self.browserOpen, url['help'])
        menu_help_reportbug = self.builder.get_object('menu_help_reportbug')
        menu_help_reportbug.connect('activate', self.browserOpen, url['reportbug'])
        menu_help_translate = self.builder.get_object('menu_help_translate')
        menu_help_translate.connect('activate', self.browserOpen, url['translate'])
 
        
        #accediendo a los controles
        #self.button = self.glade.get_object('button1')
        #self.button.connect('clicked', action)
        
    def browserOpen(self, widget, url):
        webbrowser.open(url)

    def mainQuit(self, widget):
        gtk.main_quit()

    def toggleConnection(self, widget, conn):
        
        print dir(conn)
        print conn['db']
        if conn['db']:
            conn['db'].close()
            conn['db'] = None
        else:
            self.dialog = ConnectDialog.ConnectDialog(self.appdata, self, conn)
            response = self.dialog.dialog.run()
            self.dialog.dialog.destroy()
            if response == gtk.RESPONSE_ACCEPT:
                print 'Aceptar'
            elif response == gtk.RESPONSE_REJECT:
                print 'Cancelar'
            else:
                print response
            
    def showDialog(self, widget):
        print self
        print widget
        print event
        print callback_data
        self.dialog = ConnectDialog(self.appdata)
        # widget GtkAction
        #
        #switch($widget->name) {
        #case 'menu_tools_connections':
        #$gladefile = 'connections_editor_dialog';
        #break;
        #case 'connect1':
        #case 'connect2':
        #$gladefile = 'connect_dialog';
        #break;
        #default:
        #echo $widget->name."\n";
        #return;
        #break;
        #}
        #
        #//menu_tools_connections_dialog
        #$this->dialog = new GladeXML("glade/{$gladefile}.glade");
        #//$this->dialog = $dialog->get_widget('dialog');
        #$this->dialog->signal_autoconnect_instance($this);

    def set_conn(self, conn, host, username, passwd, schema):

        #print getattr(self, "conn"+str(side))
        conn.db = _mysql.connect(host, username, passwd, schema)

        tables = self.builder.get_object('tables'+str(conn.side))
        store = gtk.ListStore(gobject.TYPE_STRING)
        tables.set_model(store)
        cell = gtk.CellRendererText()
        tables.pack_start(cell, True)
        tables.add_attribute(cell, 'text', 0)

        connectimage = getattr(self, "connectimage"+str(conn.side))
        connectimage.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)# gtk.STOCK_DISCONNECT

        label = self.builder.get_object("connection"+str(conn.side)+"_label")
        label.set_text(username+'@'+host)
        
        #mysqldiff.conn1 = _mysql.connect(host, username, passwd, schema)
        conn.db.query("""SHOW DATABASES""")
        #conn.query("""SHOW TABLES""")
        r = conn.db.use_result()
        #r=mysqldiff.conn1.store_result()
        #results = r.fetchall()
        #for row in results:
        row = r.fetch_row()
        while(row):
            iter = store.append()
            store.set_value(iter, 0, row[0][0])
            if row[0][0] == schema:
                tables.set_active_iter(iter)
            row = r.fetch_row()

    def showAbout(self, widget):
        dialog = gtk.AboutDialog()
        dialog.set_name('MySQL Diff')
        dialog.set_version('0.1 Alpha');
        dialog.set_authors([__author__])
        dialog.run()
        dialog.hide()

    def openConnectionsEditor(self, widget):
        window = connectionseditor.ConnectionsEditor()



if __name__ == "__main__":
    mysqldiff = MysqlDiff()
    gtk.main()
