import ConfigParser
import string
from persistence import Persistence

class UserData(Persistence):
    def __init__(self, appdata):
        #super(UserData, self).__init__(appdata)
        self.filename = appdata+'/defaults.ini'
        self._data = {
            'maximized': False,
            'width': 800,
            'height': 400,
        }
        #self.config = _ConfigDefault.copy()

    def load(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.filename)
        for sec in cp.sections():
            name = string.lower(sec)
            for opt in cp.options(sec):
                print "--> ", string.lower(opt), string.strip(cp.get(sec, opt))
                self._data[string.lower(opt)] = string.strip(cp.get(sec, opt))
                #self._data[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
            for opt in cp.options(sec):
                print "--> ", string.lower(opt), string.strip(cp.get(sec, opt))
        
    def save(self, config = None):
        cp = ConfigParser.ConfigParser()
        #sections = set([k.split('.')[0] for k in config.keys()])
        section_name = 'Window'
        cp.add_section(section_name)
        for k in self._data:
            #s, o = k.split('.')
            #print k, self._data[k], type(self._data[k])
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



        #print 'hola'


#        print appdata
#        self._app_data_dir
#        self._app_data_ini_file
#        self._data = {
#            'maximized': true,
#            'width': 800,
#            'height': 400,
#            'lang': 'es_UY.UTF-8',# $_SERVER['LANG'],
#        }

#        self._app_data_dir = $_SERVER['HOME'].DIRECTORY_SEPARATOR.'.bng5'.DIRECTORY_SEPARATOR.'mysqldiff';
#        $this->_app_data_ini_file = $this->_app_data_dir.DIRECTORY_SEPARATOR.'defaults.ini';
#
#        if(!file_exists($this->_app_data_dir)) {
#            mkdir($this->_app_data_dir);
#        }
#
#        if(file_exists($this->_app_data_ini_file) && is_readable($this->_app_data_ini_file)) {
#            $defaults = parse_ini_file($this->_app_data_ini_file, true);
#            $this->_data = $defaults + $this->_data;
#        }
#        else {
#            $this->_data = $this->_defaults;
#        }
#    }
#
#    public function __destruct() {
#        $fp = fopen($this->_app_data_ini_file, 'w');
#        foreach($this->_data AS $k => $v) {
#            fwrite($fp, "{$k} = {$v}\n");
#        }
#        fclose($fp);
#    }
#
#    public function window_state_event() {
#        print_r(func_get_args());
#    }
#
#    public function __get($name) {
#        return $this->_data[$name];
#    }
#
#    public function __set($name, $value) {
#        $this->_data[$name] = $value;
#    }
#}


#if __name__ == "__main__":
#    print "Hello World"
