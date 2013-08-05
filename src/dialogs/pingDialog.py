
import gtk
import glib
from subprocess import PIPE, Popen

class pingDialog(gtk.MessageDialog):
    
    def __init__(self, parent, message, host):
        #message = "Could not connect to host '"+host+"'.\nMySQL Error Nr. %d\n%s\n\nClick the 'Ping' button to see if there is a networking problem." % (e.args[0], e.args[1])
        super(pingDialog, self).__init__(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(True)
        self.set_title('')
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        #viewport = gtk.Viewport()
        #viewport.set_hadjustment(adjustment)
        #scroll.add(viewport)

        textview = gtk.TextView()
        textview.set_buffer(gtk.TextBuffer())
        textview.set_editable(False)
        #viewport.add(textview)
        scroll.add(textview)
        self.vbox.pack_end(scroll)

        ping_button = gtk.ToggleButton("_Ping Host")
        self.action_area.pack_end(ping_button)
        ping_button.connect('clicked', self.ping_host, host, textview)
        self.ping = None
        ping_button.show()

    def ping_host(self, widget, host, view):
        if widget.get_active() == False:
            self.stop_ping()
            widget.set_label('_Ping Host')
            return

        widget.set_label('Stop _Ping')
        buffer = view.get_buffer()
        buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())
        self.ping = Popen(
            ['ping', host],
            #['nc', 'localhost', '2000'],
            stdout = PIPE,
            stderr = PIPE
        )
        glib.io_add_watch(self.ping.stdout,
            glib.IO_IN,
            self.write_to_buffer,
            view)

        #out, error = ping.communicate()
        view.get_parent().show_all()
        #self.readline(self.ping, view)

    def write_to_buffer(self, fd, condition, view):
        #if condition == glib.IO_IN:
        #            r = fd.readline()#.read(1)
        #            print r
        r = fd.readline()#.read(1)
        buffer = view.get_buffer()
        iter = buffer.get_end_iter()
        buffer.insert(iter, r)
        view.scroll_to_iter(iter, 0.4, False)
        return True
        #else:
        #    return False

    def stop_ping(self):
        if self.ping:
            self.ping.terminate()
            self.ping = None
