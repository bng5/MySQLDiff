
import gtk
import gobject
from persistence import Bookmarks

class ConnectDialog:

    def __init__(self, appdata, parent, conn):
        self.builder = gtk.Builder()
        self.builder.add_from_file("glade/connect_dialog.ui")
        #self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog')
        #self.window.show_all()
        #dialog.run()
        #dialog.hide()

        self.parent = parent
        self.conn = conn

        combo = self.builder.get_object('stored_connections')
        combo.connect('changed', self.active_iter)
        #combo.set_row_separator_func(self.combo_separator)

        combo.child.set_text('holaaaaaaaaaa')
        store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)#, gobject.TYPE_BOOLEAN)

        self.bm = Bookmarks.Bookmarks(appdata)
        bookmarks = self.bm.getBookmarks()
        for sec in bookmarks:
            iterador = store.append()
            store.set_value(iterador, 0, sec)
            store.set_value(iterador, 1, bookmarks[sec])
            #store.set_value(iterador, 2, False)

        #        iterador = store.append()
        #        store.set_value(iterador, 0, '')
        #        store.set_value(iterador, 1, {})
        #        store.set_value(iterador, 2, True)
        #
        #        iterador = store.append()
        #        store.set_value(iterador, 0, 'Save This Connection...')
        #        store.set_value(iterador, 1, {})
        #        store.set_value(iterador, 2, False)
        #
        #        iterador = store.append()
        #        store.set_value(iterador, 0, 'Open Connection Editor')
        #        store.set_value(iterador, 1, {})
        #        store.set_value(iterador, 2, False)

        combo.set_model(store)
        combo.set_text_column(0)
        #        cell = gtk.CellRendererText()
        #        combo.pack_start(cell, True)
        #        combo.add_attribute(cell, 'text', 0)

        self.entry = {}
        self.entry['username'] = self.builder.get_object('username_entry')
        self.entry['pass'] = self.builder.get_object('pass_entry')
        self.entry['host'] = self.builder.get_object('host_entry')
        self.entry['port'] = self.builder.get_object('port_entry')
        self.entry['schema'] = self.builder.get_object('schema_entry')

    def combo_separator(self, model, iter):
        return False
        return model.get_value(iter, 2)

    def active_iter(self, widget):

        #print widget.get_active()
        #print widget.get_active_text()

        iter = widget.get_active_iter()
        model = widget.get_model()
        #self.entry_name.set_text(model.get_value(iter, 0))
        #        if widget.get_active() == (len(widget.get_model()) - 2):
        #            print 'save'
        #            name_entry = self.builder.get_object('name_entry')
        #            name_label = self.builder.get_object('name_label')
        #            savepassword = self.builder.get_object('savepassword_check')
        #            name_entry.show()
        #            name_label.show()
        #            savepassword.show()
        #        elif widget.get_active() == (len(widget.get_model()) - 1):
        #            self.parent.openConnectionsEditor(widget)
        #        else:
        if widget.get_active() >= 0:
            data = model.get_value(iter, 1)
            for entry in self.entry:
                self.entry[entry].set_text(data[entry])

    def connect(self, widget, data = None):
        
        host = self.builder.get_object('host_entry').get_text()
        port = self.builder.get_object('port_entry').get_value()
        username = self.builder.get_object('username_entry').get_text()
        passwd = self.builder.get_object('pass_entry').get_text()
        schema = self.builder.get_object('schema_entry').get_text();

        self.parent.set_conn(self.conn, host, username, passwd, schema)

    def close(self, widget):
        #self.dialog.destroy()
        print 'close'
