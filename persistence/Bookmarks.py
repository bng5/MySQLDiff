#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
#import string
#import array
import hashlib
import Jumble
import os.path

class Bookmarks:

    instance = None

    def __new__(cls, *args, **kargs):
        print cls
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def __init__(self, path):
        print self
        self.appdata = path+'/bookmarks.ini'
        if not os.path.exists(self.appdata):
            open(self.appdata, 'w').close()
        self.hash = self.md5File()
        self.jumble = Jumble.Jumble()
        
    def getBookmarks(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.appdata)
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
        fp = open(self.appdata, 'rb')
        for i in fp:
            crc.update(i)
        fp.close()
        return crc.hexdigest()
    
    def save(self, model):
        config = ConfigParser.ConfigParser()
        
        for row in model:
            config.add_section(row[0])
            data = row[1]
            for opt in data:
                if opt == 'pass':
                    val = self.jumble.encrypt(data[opt])
                else:
                    val = data[opt]
                config.set(row[0], opt, val)
        with open(self.appdata, 'wb') as configfile:
            config.write(configfile)
