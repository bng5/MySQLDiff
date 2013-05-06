
import sys
import os
from os import path
import gtk
import gobject

"""
Singleton Man in the middle
"""
class Presenter(object):

    instance = None

    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.instance._init()
        return cls.instance

    def _init(self, *args, **kargs):

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
        if not os.path.exists(self.appdata):
            os.makedirs(self.appdata)

    def open_url(self, widget, url):
        #print widget.get_name()
        gtk.show_uri(None, url, int(gobject.get_current_time()))