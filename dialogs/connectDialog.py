
import gtk

#from persistence import Bookmarks

class ConnectDialog(gtk.Dialog):

    def __init__(self, parent):
        self.builder = gtk.Builder()

        super(ConnectDialog, self).__init__('Connect to MySQL Server Instance', 
             parent, 
             gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
             (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
              gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        self.set_border_width(5)
        self.set_default_response(gtk.RESPONSE_ACCEPT)
        
        self.entry = {}
        
        frame = gtk.Frame('Connect to MySQL Server Instance')
        frame.set_border_width(4)
        vbox = gtk.VBox(homogeneous=False, spacing=0)
        table = gtk.Table(6, 4, False)
        
        #table.set_col_spacing(0, 20)
        table.set_col_spacings(10)
        table.set_row_spacings(10)
        table.set_border_width(10)

        label = gtk.Label('Stored Connection:')
        label.set_alignment(xalign=1.0, yalign=0.5)
        table.attach(label, 0, 1, 0, 1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        label.show()
        entry = gtk.ComboBox(model=None)
        table.attach(entry, 1, 4, 0, 1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        entry.show()
        
        hr = gtk.HSeparator()
        table.attach(hr, 0, 4, 1, 2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        hr.show()
        
        label = gtk.Label('Server Hostname:')
        label.set_alignment(xalign=1.0, yalign=0.5)
        table.attach(label, 0, 1, 2, 3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        label.show()
        self.entry['host'] = gtk.Entry(max=0)
        self.entry['host'].set_text('localhost')
        table.attach(self.entry['host'], 1, 2, 2, 3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        self.entry['host'].show()
        
        label = gtk.Label('Port:')
        label.set_alignment(xalign=1.0, yalign=0.5)
        table.attach(label, 2, 3, 2, 3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        label.show()
        adjustment = gtk.Adjustment(value=3306, lower=0, upper=65535, step_incr=1)
        self.entry['port'] = gtk.SpinButton(adjustment)
        table.attach(self.entry['port'], 3, 4, 2, 3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        self.entry['port'].show()
        
        label = gtk.Label('Username:')
        label.set_alignment(xalign=1.0, yalign=0.5)
        table.attach(label, 0, 1, 3, 4, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        label.show()
        self.entry['username'] = gtk.Entry(max=0)
        self.entry['username'].set_text('pablo')
        table.attach(self.entry['username'], 1, 2, 3, 4, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        self.entry['username'].show()
        
        label = gtk.Label('Password:')
        label.set_alignment(xalign=1.0, yalign=0.5)
        table.attach(label, 0, 1, 4, 5, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        label.show()
        self.entry['pass'] = gtk.Entry(max=0)
        #entry.caps_lock-warning = True
        self.entry['pass'].set_visibility(False)
        table.attach(self.entry['pass'], 1, 2, 4, 5, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        self.entry['pass'].show()
        
        label = gtk.Label('Default Schema:')
        label.set_alignment(xalign=1.0, yalign=0.5)
        table.attach(label, 0, 1, 5, 6, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        label.show()
        self.entry['schema'] = gtk.Entry(max=0)
        self.entry['schema'].set_text('mysql')
        table.attach(self.entry['schema'], 1, 2, 5, 6, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.FILL)
        self.entry['schema'].show()
        
        #attach(child, left_attach, right_attach, top_attach, bottom_attach, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
        
        vbox.pack_end(table)
        table.show()
        frame.add(vbox)
        vbox.show()

        self.vbox.pack_end(frame)
        frame.show()
        return
    
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
        

        combo.set_model(self.store)
        #combo.set_text_column(0)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        self.combo_active = combo.get_active()


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
