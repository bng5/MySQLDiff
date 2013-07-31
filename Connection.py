
#import _mysql
import MySQLdb

class Connection:
    def __init__(self, side):
        self.side = side
        self.connected = False
        #'menu_item': self.builder.get_object('menu_file_connect1'),
        #'button': self.builder.get_object('connect1'),
        #'label': self.builder.get_object("connection1_label"),
        self.db = None
        #'schemas_combo': self.builder.get_object('schemas_combo1'),
        #'tables_tree': self.builder.get_object('treeview1'),
        self.host = None
        self.username = None
        self.passwd = None
        self.schema = None

    def is_connected(self):
        return self.connected

    def connect(self, host, username, passwd, schema):
        print 'conectar'
        self.db = MySQLdb.connect(host, username, passwd, schema)
        self.connected = True

    def close(self):
	   print 'desconectar'
	   self.db.close()
	   self.connected = False

