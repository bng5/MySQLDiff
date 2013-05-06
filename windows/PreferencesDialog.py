
import gtk

class PreferencesDialog:

    def __init__(self):
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

    