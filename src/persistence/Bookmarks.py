#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
#import string
#import array
import gtk
import gobject
import hashlib
import Jumble
import os.path

class Bookmarks(gtk.ListStore):

    instance = None

    #    def __new__(cls, *args, **kargs):
    #        print cls
    #        if cls.instance is None:
    #            cls.instance = object.__new__(cls, *args, **kargs)
    #        return cls.instance

    def __init__(self, path):
        print 'Bookmarks'
        self.filename = path+'/bookmarks.ini'
        gtk.ListStore.__init__(self, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN)
        if not os.path.exists(self.filename):
            open(self.filename, 'w').close()
        self.hash = self.md5File()
        self.jumble = Jumble.Jumble()
    
    def load(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.filename)
        for name in cp.sections():
            data = {}
            for opt in cp.items(name):
                if opt[0] == 'pass':
                    data[opt[0]] = self.jumble.decrypt(opt[1])
                else:
                    data[opt[0]] = opt[1]
            iterador = self.append()
            self.set_value(iterador, 0, name)
            self.set_value(iterador, 1, data)
            self.set_value(iterador, 2, False)

    def getBookmarks(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.filename)
        data = {}
        for name in cp.sections():
            data[name] = {}
            for opt in cp.items(name):
                if opt[0] == 'pass':
                    data[name][opt[0]] = self.jumble.decrypt(opt[1])
                else:
                    data[name][opt[0]] = opt[1]
        return data

    def md5File(self):
        crc = hashlib.md5()
        fp = open(self.filename, 'rb')
        for i in fp:
            crc.update(i)
        fp.close()
        return crc.hexdigest()
    
    def save(self, model = None):
        config = ConfigParser.ConfigParser()

        for row in self:
            data = row[1]
            if data is None:
                continue
            config.add_section(row[0])
            for opt in data:
                if opt == 'pass':
                    val = self.jumble.encrypt(data[opt])
                else:
                    val = data[opt]
                config.set(row[0], opt, val)
        with open(self.filename, 'wb') as configfile:
            config.write(configfile)
