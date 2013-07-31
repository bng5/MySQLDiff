
import sys
from os import path
#from os import path#, environ

def get_userDataDir():
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains
        # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
        # NSApplicationSupportDirectory = 14
        # NSUserDomainMask = 1
        # True for expanding the tilde into a fully qualified path
        userDataDir = path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], 'bng5', 'mysqldiff')
    elif sys.platform == 'win32':
        userDataDir = path.join(environ['APPDATA'], 'bng5', 'mysqldiff')
    else:
        userDataDir = path.expanduser(path.join("~", '.bng5', 'mysqldiff'))
    return userDataDir

__all__ = ["UserData", "Bookmarks"]


