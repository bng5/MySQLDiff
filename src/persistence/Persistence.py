
class blaPersistence:
    def __init__(self, appdata):
        self.filename = appdata+'/defaults.ini'
        self._data = {
            'maximized': False,
            'width': 800,
            'height': 400,
            'lang': 'es_UY.UTF-8',# $_SERVER['LANG'],
            'xpos': 20,
            'ypos': 20,
        }
        #self.config = _ConfigDefault.copy()

    def load(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.filename)
        for sec in cp.sections():
            name = string.lower(sec)
            for opt in cp.options(sec):
                self._data[string.lower(opt)] = string.strip(cp.get(sec, opt))
                #self._data[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
        
    def write(self, config = None):
        """
        given a dictionary with key's of the form 'section.option: value'
        write() generates a list of unique section names
        creates sections based that list
        use config.set to add entries to each section
        """
        cp = ConfigParser.ConfigParser()
        #sections = set([k.split('.')[0] for k in config.keys()])
        section_name = 'Window'
        cp.add_section(section_name)
        for k in self._data:
            #s, o = k.split('.')
            print k
            print type(self._data[k])
            cp.set(section_name, k, self._data[k])
        cp.write(open(self.filename, "w"))

    @property
    def maximized(self):
        return (self._data['maximized'] == 'True')

    @property
    def width(self):
        return int(self._data['width'])

    @property
    def height(self):
        return int(self._data['height'])

    def get(self, attr):
        return self._data[attr]

    def set(self, attr, value):
        self._data[attr] = value
        return self

    #    @my_attr.setter
    #    def my_attr(self, value):
    #        pass


#if __name__=="__main__":
#    print UserData("some.ini", _ConfigDefault)
