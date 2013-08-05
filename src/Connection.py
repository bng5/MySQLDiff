
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

    def connect(self, host, username, passwd, schema = ''):
        print 'conectar'
        self.db = MySQLdb.connect(host, username, passwd, schema)
        self.connected = True
        self.host = host
        self.username = username

    def close(self):
	   print 'desconectar'
	   self.db.close()
	   self.connected = False

    def get_schemas(self):
        self.db.query("""SHOW DATABASES""")
        r = self.db.use_result()
        #r = self.db.store_result()
        #results = r.fetchall()
        #for row in results:
        #    print row
        schemas = []
        row = r.fetch_row()
        #active = None
        while(row):
            schemas.append(row[0][0])
            row = r.fetch_row()
            #iter = store.append()
            #store.set_value(iter, 0, row[0][0])
            #if row[0][0] == schema:
            #    active = iter
            #    row = r.fetch_row()
            #if active:
            #    tables.set_active_iter(active)
            #else:
            #conn['menu_item'].set_active(False)
            #self.dialog.dialog.destroy()
        return schemas

    def set_schema(self, schema):
        #conn['tables_tree'].set_visible(True)
        self.db.query("USE %s" % (schema))
        self.schema = schema
        #conn['db'].execute("""USE """+schema)
        #cursor.close()
        return self
        
    def get_tables(self):
        print 'get tables'
        self.db.query("""SHOW TABLES""")
        #self.db.query("SELECT `TABLE_NAME`, `COLUMN_NAME`, `ORDINAL_POSITION`, `COLUMN_DEFAULT`, `IS_NULLABLE`, `DATA_TYPE`, `CHARACTER_MAXIMUM_LENGTH`, `CHARACTER_OCTET_LENGTH`, `NUMERIC_PRECISION`, `NUMERIC_SCALE`, `CHARACTER_SET_NAME`, `COLLATION_NAME`, `COLUMN_TYPE`, `COLUMN_KEY`, `EXTRA`, `COLUMN_COMMENT` FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA = '%s' ORDER BY TABLE_NAME, ORDINAL_POSITION" % (schema))
        r = self.db.use_result()
        tables = []
        row = r.fetch_row()
        while(row):
            tables.append(row[0][0])
            row = r.fetch_row()
        #tables = conn['tables_tree'].get_model()
        #self.clean_tree_side(tables, side)
        return tables
