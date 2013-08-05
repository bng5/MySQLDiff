
import gtk

from persistence import Bookmarks

class ConnectDialog:

    def __init__(self, appdata, parent, conn, presenter):
        self.builder = gtk.Builder()
        
        self.builder.add_from_file("glade/connect_dialog_w.ui")
        #self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog')
        #self.window.show_all()
        #dialog.run()
        #dialog.hide()

        self.dialog.connect('close', self.d_close)
        self.dialog.connect('response', self.d_response)
        self.dialog.connect("delete_event", self.delete_event)

        self.parent = parent
        self.conn = conn

        combo = self.builder.get_object('stored_connections')
        combo.connect('changed', self.active_iter)
        combo.set_row_separator_func(self.combo_separator)

        self.store = Bookmarks.Bookmarks(appdata)
        self.store.load()

        iterador = self.store.append()
        self.store.set_value(iterador, 0, '')
        self.store.set_value(iterador, 1, None)
        self.store.set_value(iterador, 2, True)

        iterador = self.store.append()
        self.store.set_value(iterador, 0, 'Save This Connection...')
        self.store.set_value(iterador, 1, None)
        self.store.set_value(iterador, 2, False)
        
        #        iterador = store.append()
        #        store.set_value(iterador, 0, 'Open Connection Editor')
        #        store.set_value(iterador, 1, {})
        #        store.set_value(iterador, 2, False)


        combo.set_model(self.store)
        #combo.set_text_column(0)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        self.combo_active = combo.get_active()

        self.entry = {}
        self.entry['username'] = self.builder.get_object('username_entry')
        self.entry['pass'] = self.builder.get_object('pass_entry')
        self.entry['host'] = self.builder.get_object('host_entry')
        self.entry['port'] = self.builder.get_object('port_entry')
        self.entry['schema'] = self.builder.get_object('schema_entry')

    def combo_separator(self, model, iter):
        return model.get_value(iter, 2)

    def d_close(self, widget):
        print 'close'

    def d_response(self, widget, response_id):
        if response_id == gtk.RESPONSE_ACCEPT:
            self.store.save()


    def active_iter(self, widget):

        #print widget.get_active()
        #print widget.get_active_text()
        #self.entry_name.set_text(model.get_value(iter, 0))

        if widget.get_active() == -1:
            pass
        elif widget.get_active() == (len(widget.get_model()) - 1):

            #dialog = self.builder.get_object('name_dialog')
            #dialog.show_all()
            #dialog.run()
            #dialog.hide()
            widget.set_active(self.combo_active)
            dialog = gtk.Dialog("Save Connection",
                None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            dialog.set_border_width(5)
            dialog.vbox.set_spacing(2)
            dialog.vbox.pack_start(gtk.Label("Type in a name for the connection to be saved."))
            entry_name = gtk.Entry()
            dialog.vbox.pack_start(entry_name)
            save_password = gtk.CheckButton("Save Password")
            dialog.vbox.pack_start(save_password)
            dialog.show_all()
            dialog.connect('close', self.d_close)
            dialog.connect('response', self.d_response)
            if dialog.run() == gtk.RESPONSE_ACCEPT:
                model = widget.get_model()
                iterador = model.prepend()#insert(1)
                # TODO Trim y verificar nombre
                name = entry_name.get_text().strip()
                model.set_value(iterador, 0, name)
                # TODO Cargar con datos del formulario
                data = {}
                for entry in self.entry:
                    data[entry] = self.entry[entry].get_text()
                model.set_value(iterador, 1, data)
                model.set_value(iterador, 2, False)
                self.combo_active = 0
                widget.set_active(self.combo_active)
                print save_password.get_active()
            dialog.destroy()

        #elif widget.get_active() == (len(widget.get_model()) - 1):
        #    self.parent.openConnectionsEditor(widget)
        else:
            self.combo_active = widget.get_active()
            iter = widget.get_active_iter()
            model = widget.get_model()
            data = model.get_value(iter, 1)
            print self.entry
            for entry in self.entry:
                if data[entry] is None:
                    data[entry] = ''
                self.entry[entry].set_text(data[entry])

    def close(self, widget):
        #self.dialog.destroy()
        print 'close'

    def delete_event(self, widget,c):
        print c
        return False
