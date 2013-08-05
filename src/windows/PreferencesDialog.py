
import gtk

class PreferencesDialog(gtk.Dialog):

    def __init__(self):
        
        super(PreferencesDialog, self).__init__('Preferencias',
                     None,
                     0,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                      gtk.STOCK_APPLY, gtk.RESPONSE_ACCEPT))
        return
        self.builder = gtk.Builder()
        
        self.builder.add_from_file("glade/preferences_dialog.ui")
        #self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.connect('destroy', gtk.main_quit)
        self.window.show_all()
        gtk.main()
        #self.window.show_all()
        #dialog.run()
        #dialog.hide()
