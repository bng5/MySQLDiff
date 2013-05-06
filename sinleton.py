
import sys
import os
from os import path

class Singleton (object):
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

#Usage
mySingleton1 = Singleton()
print mySingleton1.appdata

mySingleton2 = Singleton()
print mySingleton1.appdata
print mySingleton2.appdata

#mySingleton1 y mySingleton2 son la misma instancia
assert mySingleton1 is mySingleton2
