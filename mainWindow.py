#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import constants

import sys
from os import path#, environ
import _mysql
import MySQLdb
import ui
import connectionseditor
import Connection

import pixmaps



#import persistence
from persistence import *


# para ping
#import subprocess

#from threading import Timer

import Presenter

from windows import ConnectDialog

## Para el Ping
## Non blocking Popen
#import sys
#from subprocess import PIPE, Popen
#from threading  import Thread
#
#try:
#    from Queue import Queue, Empty
#except ImportError:
#    from queue import Queue, Empty  # python 3.x
#
#ON_POSIX = 'posix' in sys.builtin_module_names
#
#def enqueue_output(out, queue):
#    for line in iter(out.readline, b''):
#        queue.put(line)
#    out.close()
#
#p = Popen(['myprogram.exe'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
#q = Queue()
#t = Thread(target=enqueue_output, args=(p.stdout, q))
#t.daemon = True # thread dies with the program
#t.start()
#
## ... do other things here
#
## read line without blocking
#try:  line = q.get_nowait() # or q.get(timeout=.1)
#except Empty:
#    print('no output yet')
#else: # got line
#    # ... do something with line



"""
# Probado
# Para el Ping
# Non blocking Popen
import sys
from threading  import Thread, Timer

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, err, queue):
    print 'enqueue_output'
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

#ping', '-c', '10', 'google.com
#/home/pablo/php/recibe
#p = Popen(['ping', '-c', '10', 'google.com'], stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=ON_POSIX)
#q = Queue()
#t = Thread(target=enqueue_output, args=(p.stdout, p.stderr, q))
#t.daemon = True # thread dies with the program
#t.start()




def hello():

    if ping.poll() is None:
        #process.stdin.write('%d\n' % i)
        print ping.stdout.readline().rstrip()
        t = Timer(.7, hello)
        t.start()
    else:
        print ping.stdout.read()
    return
    # read line without blocking
    try:
        line = q.get_nowait() # or q.get(timeout=.1)
    except Empty:
        print('--> no output yet')
    else: # got line
        print '--> '+line.rstrip()
    t = Timer(.5, hello)
    t.start()


ping = Popen(
    ["ping",
    "-c", "6",
    'google.com'],
    stdout = PIPE,
    stderr = PIPE
)
#out, error = ping.communicate()

t = Timer(.5, hello)
t.start()

"""





#class MainWindow(gtk.Window):
class MainWindow(gtk.Window):

    ## Colores
    COLOR_MISSING = '#FFA0B4'
    COLOR_NEW = '#B4FFB4'
    COLOR_DIFF = '#A0C8FF'

    LSIDE = -1
    RSIDE = 1

    COLUMNS = {
        -1: {
            'title': 1,
            'img': 2,
            'bgcolor': 3,
            'data': 4
        },
        1: {
            'title': 5,
            'img': 6,
            'bgcolor': 7,
            'data': 8
        }
    }

    def __init__(self, maximized = False, width = 800, height = 400):
        
        super(MainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_title('MySQL Diff')
        #self.set_size_request(width, height)
        #self.resize(width, height)
        
        self.presenter = Presenter.Presenter()

        self.appdata = self.presenter.appdata


        self.data = UserData.UserData(self.appdata)
        self.data.load()

        if maximized:
            self.maximize()
        self.set_position(gtk.WIN_POS_CENTER)
        
        self.connections = {
            constants.LSIDE: Connection.Connection(constants.LSIDE),
            constants.RSIDE: Connection.Connection(constants.RSIDE),
        }
        
        vbox = gtk.VBox()
        vbox.pack_start(self.create_menu_bar(), False, True)
        vbox.pack_start(self.create_main_area(), True, True)

        statusbar = gtk.Statusbar()
        vbox.pack_start(statusbar, False, True)
        statusbar.show()

        vbox.show()
        self.add(vbox)
    
        self.show_all()
        
    def iinit(self):
        self.schemas_combo(self.side[self.LSIDE]['schemas_combo'])
        self.schemas_combo(self.side[self.RSIDE]['schemas_combo'])
        self.side[self.LSIDE]['schemas_combo'].connect('changed', self.set_schema, self.LSIDE)
        self.side[self.RSIDE]['schemas_combo'].connect('changed', self.set_schema, self.RSIDE)

        is_table = gobject.TYPE_BOOLEAN
        tables1 = gtk.TreeStore(is_table,
            gobject.TYPE_STRING, gtk.gdk.Pixbuf, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT,
            gobject.TYPE_STRING, gtk.gdk.Pixbuf, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)

        tables2 = gtk.TreeStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf, gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        #tables = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)

        self.side[self.LSIDE]['tables_tree'].set_model(tables1)
        self.side[self.LSIDE]['tables_tree'].connect('row-expanded', self.expand_row, self.side[self.RSIDE])
        self.side[self.LSIDE]['tables_tree'].connect('row-collapsed', self.collapse_row, self.side[self.RSIDE])
        self.side[self.LSIDE]['tables_tree'].connect('cursor-changed', self.cursor_changed, self.side[self.RSIDE])
        self.side[self.LSIDE]['tables_tree'].set_visible(False)

        columna = gtk.TreeViewColumn()
        #columna.set_visible(False)
        col_cell_img = gtk.CellRendererPixbuf()
        col_cell_text = gtk.CellRendererText()
        columna.pack_start(col_cell_img, False)
        columna.pack_start(col_cell_text, True)
        columna.add_attribute(col_cell_text, "text", 1)
        columna.add_attribute(col_cell_text, "background", 3)
        columna.add_attribute(col_cell_img, "pixbuf", 2)
        #columna.add_attribute(col_cell_img, "background", 3)

        self.side[self.LSIDE]['tables_tree'].set_headers_visible(False)
        self.side[self.LSIDE]['tables_tree'].append_column(columna)

        self.side[self.RSIDE]['tables_tree'].set_model(tables1)
        self.side[self.RSIDE]['tables_tree'].connect('row-expanded', self.expand_row, self.side[self.LSIDE])
        self.side[self.RSIDE]['tables_tree'].connect('row-collapsed', self.collapse_row, self.side[self.LSIDE])
        self.side[self.RSIDE]['tables_tree'].connect('cursor-changed', self.cursor_changed, self.side[self.LSIDE])
        self.side[self.RSIDE]['tables_tree'].set_visible(False)

        columna = gtk.TreeViewColumn()
        #columna.set_visible(False)
        col_cell_img = gtk.CellRendererPixbuf()
        col_cell_text = gtk.CellRendererText()
        columna.pack_start(col_cell_img, False)
        columna.pack_start(col_cell_text, True)
        columna.add_attribute(col_cell_text, "text", 5)
        columna.add_attribute(col_cell_text, "background", 7)
        columna.add_attribute(col_cell_img, "pixbuf", 6)
        #columna.add_attribute(col_cell_img, "background", 7)

        self.side[self.RSIDE]['tables_tree'].set_headers_visible(False)
        self.side[self.RSIDE]['tables_tree'].append_column(columna)

        #selection = self.treeview.get_selection()
        
        #self.conn1.button.connect('clicked', self.showConnectDialog, 1)

 
        #accediendo a los controles
        #self.button = self.glade.get_object('button1')
        #self.button.connect('clicked', action)

    def attach_delegation(self, observer):
        self._presenter = observer

    def notify(self, event_name, data = None):
        self._presenter.notify(event_name, data)
        
    def cursor_changed(self, widget, other_side):
        path, column = widget.get_cursor()
        path2, column = other_side['tables_tree'].get_cursor()
        print path, path2
        if path != path2:
            other_side['tables_tree'].set_cursor(path, None, False)

    def expand_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].expand_row(path, False)#get_column(path[0])

    def collapse_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].collapse_row(path)

    def cursor_changed(self, widget, other_side):
        path, column = widget.get_cursor()
        path2, column = other_side['tables_tree'].get_cursor()
        print path, path2
        if path != path2:
            other_side['tables_tree'].set_cursor(path, None, False)

    def expand_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].expand_row(path, False)#get_column(path[0])

    def collapse_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].collapse_row(path)

    def cursor_changed(self, widget, other_side):
        path, column = widget.get_cursor()
        path2, column = other_side['tables_tree'].get_cursor()
        print path, path2
        if path != path2:
            other_side['tables_tree'].set_cursor(path, None, False)

    def expand_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].expand_row(path, False)#get_column(path[0])

    def collapse_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].collapse_row(path)

    def cursor_changed(self, widget, other_side):
        path, column = widget.get_cursor()
        path2, column = other_side['tables_tree'].get_cursor()
        print path, path2
        if path != path2:
            other_side['tables_tree'].set_cursor(path, None, False)

    def expand_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].expand_row(path, False)#get_column(path[0])

    def collapse_row(self, widget, iter, path, other_side):
        other_side['tables_tree'].collapse_row(path)

    def persist(self):
        self.data.write()

    def toggled_menu_item(self, widget, conn):
        if conn['connected'] != widget.get_active():
            self.toggleConnection(widget, conn)

    def toggleConnection(self, widget, conn):

        print 'toggleConnection', conn
        self.notify('connect', conn)

        return
    
    
        if conn['connected']:
            conn['connected'] = False
            conn['menu_item'].set_active(False)
            conn['label'].set_text('Not connected')
            conn['db'].close()
            conn['db'] = None
            conn['button'].set_tooltip_text("Connect")
            conn['button'].child.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_BUTTON)
            conn['schemas_combo'].get_model().clear()
            conn['tables_tree'].get_model().clear()
            conn['tables_tree'].set_visible(False)
        else:
            self.dialog = ConnectDialog.ConnectDialog(self.appdata, self, conn, self.presenter)
            while self.dialog.dialog.run() == gtk.RESPONSE_ACCEPT:
                #print 'while'
                #if self.dialog.dialog.run() == gtk.RESPONSE_ACCEPT:
                username = self.dialog.entry['username'].get_text()
                passwd = self.dialog.entry['pass'].get_text()
                host = self.dialog.entry['host'].get_text()
                port = self.dialog.entry['port'].get_value_as_int()
                schema = self.dialog.entry['schema'].get_text()

                #conn['db'] = _mysql.connect(host, username, passwd, schema)
                print conn['db']
                try:
                    conn['db'] = MySQLdb.connect(host, username, passwd, schema)
                except MySQLdb.Error, e:
                    #self.dialog.dialog.destroy()
                    #self.show_dialog("Could not connect to host '"+host+"'.\nMySQL Error Nr. %d\n%s" % (e.args[0], e.args[1]), '', gtk.MESSAGE_ERROR)
                    dialog = gtk.MessageDialog(self.dialog.dialog, gtk.DIALOG_MODAL,
                        gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                        "Could not connect to host '"+host+"'.\nMySQL Error Nr. %d\n%s\n\nClick the 'Ping' button to see if there is a networking problem." % (e.args[0], e.args[1]))
                    #dialog.set_title('')
                    dialog.set_position(gtk.WIN_POS_CENTER)

                    scroll = gtk.ScrolledWindow()

                    textview = gtk.TextView()
                    textview.set_buffer(gtk.TextBuffer())
                    textview.set_editable(False)
                    scroll.add(textview)
                    dialog.vbox.pack_end(scroll)

                    ping_button = gtk.ToggleButton("_Ping Host")
                    dialog.action_area.pack_end(ping_button)
                    ping_button.connect('clicked', self.ping_host, host, textview)
                    self.ping = None
                    ping_button.show()
                    dialog.run()
                    self.stop_ping()
                    dialog.destroy()
                    conn['menu_item'].set_active(False)
                    continue


                #conn['db'] = MySQLdb.connect(host = _host, port = _port, user = _username, passwd = _passwd, db = _schema)
                #                cursor = _c.cursor()
                #                cursor.execute("SELECT VERSION()")
                #                row = cursor.fetchone ()
                #                print "server version:", row[0]
                #                cursor.close()
                #                _c.close()

                conn['connected'] = True
                conn['menu_item'].set_active(True)
                conn['label'].set_text(username+'@'+host)
                conn['button'].set_tooltip_text("Disconnect")
                conn['button'].child.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)# gtk.STOCK_DISCONNECT

                tables = conn['schemas_combo']
                store = tables.get_model()
                conn['db'].query("""SHOW DATABASES""")
                #conn.query("""SHOW TABLES""")
                r = conn['db'].use_result()
                #r=mysqldiff.conn1.store_result()
                #results = r.fetchall()
                #for row in results:
                row = r.fetch_row()
                active = None
                while(row):
                    iter = store.append()
                    store.set_value(iter, 0, row[0][0])
                    if row[0][0] == schema:
                        active = iter
                    row = r.fetch_row()
                if active:
                    tables.set_active_iter(active)
            else:
                conn['menu_item'].set_active(False)
            self.dialog.dialog.destroy()

    def set_schema(self, widget, side):

        if widget.get_active() == -1:
            return

        iter = widget.get_active_iter()
        model = widget.get_model()
        schema = model.get_value(iter, 0)
        #cursor = conn['db'].cursor()
        conn = self.side[side]
        conn['tables_tree'].set_visible(True)
        conn['db'].query("USE %s" % (schema))
        #conn['db'].execute("""USE """+schema)
        #cursor.close()
        #conn['db'].query("""SHOW TABLES""")
        conn['db'].query("SELECT `TABLE_NAME`, `COLUMN_NAME`, `ORDINAL_POSITION`, `COLUMN_DEFAULT`, `IS_NULLABLE`, `DATA_TYPE`, `CHARACTER_MAXIMUM_LENGTH`, `CHARACTER_OCTET_LENGTH`, `NUMERIC_PRECISION`, `NUMERIC_SCALE`, `CHARACTER_SET_NAME`, `COLLATION_NAME`, `COLUMN_TYPE`, `COLUMN_KEY`, `EXTRA`, `COLUMN_COMMENT` FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA = '%s' ORDER BY TABLE_NAME, ORDINAL_POSITION" % (schema))
        r = conn['db'].use_result()
        row = r.fetch_row()
        tables = conn['tables_tree'].get_model()
        self.clean_tree_side(tables, side)
        #tables.clear()
        table_name = ''
        i = 0
        t = 0
        if self.LSIDE == side:
            title_compare_k = 5
        else:
            title_compare_k = 1
        while(row):
            bgcolor = None
            if table_name != row[0][0]:
                table = tables.iter_nth_child(None, t)
                if table:
                    #if tables.get_value(table, title_compare_k) == '':
                    #    tables.remove(table)
                    #    continue
                    comp = cmp(row[0][0], tables.get_value(table, title_compare_k))
                    if comp == -1:
                        print '    Agregando antes'
                        table = tables.insert_before(None, table, [True, '', None, self.COLOR_MISSING, {}, '', None, self.COLOR_MISSING, {}])
                        bgcolor = self.COLOR_NEW
                        t = t + 1
                    elif comp == 1:
                        t = t + 1
                        tables.set_value(table, self.COLUMNS[side]['bgcolor'], self.COLOR_MISSING)
                        continue
                    else:
                        t = t + 1
                else:
                    table = tables.append(None, [True, '', None, None, {}, '', None, None, {}])
                    t = t + 1
                table_name = row[0][0]

                tables.set_value(table, self.COLUMNS[side]['title'], row[0][0])
                tables.set_value(table, self.COLUMNS[side]['img'], pixmaps.table)
                tables.set_value(table, self.COLUMNS[side]['bgcolor'], bgcolor)
                tables.set_value(table, self.COLUMNS[side]['data'], {})

                #table = tables.append(None, data)
            #img = pixmaps.table# if is_folder else pixmaps.field

            if self.LSIDE == side:
                data = [False, row[0][1], pixmaps.field, None, {}, 'Missing', None, None, {}]
            else:
                data = [False, 'Missing', None, None, {}, row[0][1], pixmaps.field, None, {}]
            tables.append(table, data)

            #iterador = tables.append()
            #tables.set_value(iterador, 0, row[0][0])
            #tables.set_value(iterador, 1, row[0][0]+'_columna')

            #self.model.set_value(iterador, 1, bookmarks[sec])
            #iter = store.append()
            #store.set_value(iter, 0, row[0][0])
            #if row[0][0] == schema:
            #    tables.set_active_iter(iter)
            row = r.fetch_row()
            i = i + 1

    def readline(self, process, view):
        if process:
            if process.poll() is None:
                #process.stdin.write('%d\n' % i)
                r = self.ping.stdout.readline()#.rstrip()
                print r
                buffer = view.get_buffer()
                iter = buffer.get_end_iter()
                buffer.insert(iter, r)
                view.scroll_to_iter(iter, 0.4, False)
                gobject.timeout_add_seconds(1, self.readline, process, view)
            else:
                print self.ping.stdout.read()

    def ping_host_twisted(self, widget, host, dialog):
        from twisted.internet import protocol, reactor

        class MyProcessProtocol(protocol.ProcessProtocol):

            def connectionMade(self):
                print "connectionMade!"
                self.transport.closeStdin()

            def outReceived(self, data):
                print data

            def processEnded(self, reason):
                print "processEnded, status %d" % (reason.value.exitCode,)
                print "quitting"
                reactor.stop()

        proc = MyProcessProtocol()
        reactor.spawnProcess(proc, 'ping', ['ping', '-c', '15', host])
        reactor.run()

    def ping_host_vte(self, widget, host, dialog):
        import vte
        v = vte.Terminal()
        dir(v)
        v.connect("child-exited", lambda term: gtk.main_quit())
        v.fork_command()
        dialog.vbox.pack_end(v)
        v.show()
        v.feed_child('ping '+host+'\n')


    def ping_host0(self, widget, host):
        #if self.ping:
        if widget.get_active() == False:
            print 'KILL'
            self.ping.kill()
            print self.ping.stdout.readline()
            self.ping = None
            widget.set_label('_Ping Host')
            return

        widget.set_label('Stop _Ping')
        self.ping = subprocess.Popen(
            ["ping", #"-c", "10",
            host],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        #out, error = ping.communicate()
        while self.ping.poll() is None:
            #process.stdin.write('%d\n' % i)
            print self.ping.stdout.readline().rstrip()
        #print out
        #print error
        #return out

    def clean_tree_side(self, tables, side):

        t = 0
        #table = tables.get_iter_first()
        table = tables.iter_nth_child(None, t)
        while table:
            tables.set_value(table, self.COLUMNS[side]['title'], '')
            tables.set_value(table, self.COLUMNS[side]['img'], None)
            tables.set_value(table, self.COLUMNS[side]['data'], None)

            if tables.get_value(table, 1) == '' and tables.get_value(table, 5) == '':
                tables.remove(table)
            else:
                t = t + 1
            #table = tables.iter_next(table)
            table = tables.iter_nth_child(None, t)

    def create_menu_bar(self):
        options = (
            {
                'label': '_Archivo',
                'options': (
                    {
                        'stock': gtk.STOCK_QUIT,
                        'label': 'ca',
                        #'callback': lambda widget, event: self.destroy(),
                        #'callback': lambda widget, event: self.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))
                        'callback': self.mainQuit,
                    },
                ),
            },
            {
                'label': '_Tools',
                'options': (
                    {
                        'stock': gtk.STOCK_PREFERENCES,
                        'label': 'ba',
                        'callback': self.openPreferences,
                    },
                ),

            },
            {
                'label': 'Ay_uda',
                'options': (
                    {
                        'stock': gtk.STOCK_ABOUT,
                        'label': 'cb',
                        'callback': lambda widget, data: ui.about(),
                    },
                ),

            },
        );

        menubar = gtk.MenuBar()
        for item in options:
            menuitem = gtk.MenuItem(item['label'])
            filemenu = gtk.Menu()
            menuitem.set_submenu(filemenu)
            for subitem in item['options']:
                #submenuitem = gtk.MenuItem(subitem)
                submenuitem = gtk.ImageMenuItem(subitem['stock'])
                submenuitem.connect("activate", subitem['callback'], 'qwerty')
            filemenu.append(submenuitem)
            menubar.append(menuitem)
            menuitem.show()

        menubar.show()
        return menubar

    def create_main_area(self):

        alignment = gtk.Alignment(0.0, 0.0, 1.0, 1.0)
        vbox = gtk.VBox()

        alignment.add(vbox)

        alignment2 = gtk.Alignment(0.0, 0.0, 1.0, 1.0)
        table = gtk.Table(2, 3)
        cell1 = gtk.HBox()
        label1 = gtk.Label('Not connected')
        cell1.pack_start(label1, False, False, 6)
        connect1 = gtk.Button()
        image1 = gtk.Image()
        image1.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)
        connect1.add(image1)
        connect1.connect('clicked', self.toggleConnection, self.connections[self.LSIDE])
        #self.side[self.LSIDE]['button'].connect('clicked', self.toggleConnection, self.side[self.LSIDE])
        cell1.pack_start(connect1, False, True)
        table.attach(cell1, 0, 1, 0, 1)
        cell2 = gtk.HBox()
        label2 = gtk.Label('Not connected')
        cell2.pack_start(label2, False, False, 6)
        connect2 = gtk.Button()
        image2 = gtk.Image()
        image2.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)
        connect2.add(image2)
        connect2.connect('clicked', self.toggleConnection, self.connections[constants.RSIDE])
        #self.side[self.RSIDE]['button'].connect('clicked', self.toggleConnection, self.side[self.RSIDE])
        cell2.pack_start(connect2, False, True)
        table.attach(cell2, 2, 3, 0, 1)
        alignment2.add(table)
        vbox.pack_start(alignment2, False, True)
        alignment2.show()
        
        vpaned = gtk.VPaned()
        scrolledWindow = gtk.ScrolledWindow()
        vpaned.add1(scrolledWindow)

        textview = gtk.TextView()
        vpaned.add2(textview)
        
        vbox.pack_start(vpaned, True, True)
        vpaned.show()
        
        buttonbox = gtk.HButtonBox()
        b1 = gtk.Button('botón 1')
        buttonbox.pack_start(b1, False, False)
        b2 = gtk.Button('botón 2')
        buttonbox.pack_start(b2, False, False)
        b3 = gtk.Button('botón 3')
        buttonbox.pack_start(b3, False, False)
        vbox.pack_start(buttonbox, False, True)
        buttonbox.show()
        
        alignment.show()
        return alignment


    #    def show_dialog(self, message, title = 'Confirm', type = gtk.MESSAGE_INFO):
    #        dialog = gtk.MessageDialog(self._window, gtk.DIALOG_MODAL,
    #            type, gtk.BUTTONS_OK_CANCEL,
    #            message)
    #        # gtk.MESSAGE_INFO, gtk.MESSAGE_WARNING, gtk.MESSAGE_QUESTION or gtk.MESSAGE_ERROR
    #        dialog.set_title(title)
    #        dialog.set_position(gtk.WIN_POS_CENTER)
    #        response = dialog.run()
    #        dialog.destroy()
    #        return (response == gtk.RESPONSE_OK)

    def openConnectionsEditor(self, widget):
        window = connectionseditor.ConnectionsEditor()

    def openPreferences(self, widget, event, data = None):
        self.notify('open-preferences')

    def schemas_combo(self, combo):
        combo.set_model(gtk.ListStore(gobject.TYPE_STRING))
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)

    def mainQuit(self, widget, event):
        self.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))
        self.destroy()
