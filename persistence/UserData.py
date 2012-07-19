import ConfigParser
import string


class UserData:
    def __init__(self, appdata):
        self._data = {
                'maximized': True,
                'width': 800,
                'height': 400,
                'lang': 'es_UY.UTF-8',# $_SERVER['LANG'],
            }
        #self.config = _ConfigDefault.copy()
        cp = ConfigParser.ConfigParser()
        cp.read(appdata+'/defaults.ini')
        for sec in cp.sections():
            name = string.lower(sec)
            for opt in cp.options(sec):
                self._data[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
        print self._data
    def write(self, filename, config):
        """
        given a dictionary with key's of the form 'section.option: value'
        write() generates a list of unique section names
        creates sections based that list
        use config.set to add entries to each section
        """
        cp = ConfigParser.ConfigParser()
        sections = set([k.split('.')[0] for k in config.keys()])
        map(cp.add_section, sections)
        for k,v in config.items():
            s, o = k.split('.')
            cp.set(s, o, v)
        cp.write(open(filename, "w"))

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
