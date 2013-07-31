#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import constants
import persistence
#from persistence import UserData
import mainWindow
from windows import MainWindow
from windows import PreferencesDialog
from windows import ConnectDialog
from dialogs import *

class Presenter:
    def __init__(self):
        self.userDataDir = persistence.get_userDataDir()
        
    def main(self):
        self.userData = persistence.UserData.UserData(self.userDataDir)
        self.userData.load()
        


        #bookmarks = Bookmarks.Bookmarks(userDataDir)
        #bookmarks.load()
        
        self.window = mainWindow.MainWindow(self.userData.maximized, self.userData.width, self.userData.height)
        self.window.connect("delete_event", self.main_delete)
        self.window.connect("destroy", self.main_quit)
        self.window.connect("window-state-event", self.on_window_state_event)
        self.window.attach_delegation(self)
        
        window_glade = MainWindow.MainWindow()
        #window.main()
        
        gtk.main()

    def notify(self, event_name, data = None):
        print event_name
        if event_name == 'open-preferences':
            dialog = PreferencesDialog.PreferencesDialog()
            dialog.run()
            dialog.destroy()
        elif event_name == 'connect':
            self.connect(data)
        """
            print "You typed zero.\n"
        elif n== 1 or n == 9 or n == 4:
            print "n is a perfect square\n"
        elif n == 2:
            print "n is an even number\n"
        elif  n== 3 or n == 5 or n == 7:
            print "n is a prime number\n"
        """
        
    def connect(self, conn):
        if conn.is_connected():
            conn.close()
        else:
            host = 'localhost'
            try:
                conn.connect(host, username = 'pablo', passwd = '98970', schema = 'mysql')
            except Exception, e:
                dialog = pingDialog.pingDialog(self.window, "Could not connect to host '"+host+"'.\nMySQL Error Nr. %d\n%s\n\nClick the 'Ping' button to see if there is a networking problem." % (e[0], e[1]), host)
                dialog.run()
                #self.stop_ping()
                dialog.stop_ping()
                dialog.destroy()
                print 'dialog destroy'
                #conn['menu_item'].set_active(False)
                return False
        
    def main_delete(self, widget, event, data = None):
        print 'delete-event'
        w, h = widget.get_window().get_size()
        self.userData.set('width', w)
        self.userData.set('height', h)
        return False
        
    def main_quit(self, widget):
        print 'destroy'
        self.userData.save()
        gtk.main_quit()
        
    def on_window_state_event(self, widget, event, data = None):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED
        self.userData.set('maximized', widget.get_window().get_state() & mask == mask)

if __name__ == "__main__":
    presenter = Presenter()
    presenter.main()
