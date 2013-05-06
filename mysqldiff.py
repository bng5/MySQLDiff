import Presenter
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
#import gobject
#import sys
#import os
#from os import path

#import connectionseditor
from windows import MainWindow


#import persistence
#from persistence import *


__author__="Pablo Bangueses"

if __name__ == "__main__":
    #print sys.argv

    #presenter = Presenter.Presenter()
    #presenter.show_window(MainWindow.MainWindow())
    window = MainWindow.MainWindow()
    gtk.main()
