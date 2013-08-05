#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import glib
import sys
from os import path#, environ
import _mysql
import MySQLdb
import connectionseditor
import PreferencesDialog
import ConnectDialog

import pixmaps

import gobject

#import persistence
from persistence import *


import Presenter

class MainWindow:

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

    def __init__(self):

        #print bm.getBookmarks()


        self.presenter = Presenter.Presenter()

        self.appdata = self.presenter.appdata


        self.data = UserData.UserData(self.appdata)
        self.data.load()
        
        self.builder = gtk.Builder()
        self.builder.add_from_file("glade/main_window.ui")
        self.window = self.builder.get_object('window')
        #self.builder.connect_signals(self)

        #self.window.set_size_request(self.data.get('width'), self.data.get('height'))
        if self.data.maximized:
            self.window.maximize()

        self.window.show_all()

        self.side = {}
        self.side[self.LSIDE] = {
            'connected': False,
            'menu_item': self.builder.get_object('menu_file_connect1'),
            'button': self.builder.get_object('connect1'),
            'label': self.builder.get_object("connection1_label"),
            'db': None,
            'schemas_combo': self.builder.get_object('schemas_combo1'),
            'tables_tree': self.builder.get_object('treeview1')
        }
        self.side[self.RSIDE] = {
            'connected': False,
            'menu_item': self.builder.get_object('menu_file_connect2'),
            'button': self.builder.get_object('connect2'),
            'label': self.builder.get_object("connection2_label"),
            'db': None,
            'schemas_combo': self.builder.get_object('schemas_combo2'),
            'tables_tree': self.builder.get_object('treeview2')
        }

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
        self.side[self.LSIDE]['button'].connect('clicked', self.toggleConnection, self.side[self.LSIDE])
        self.side[self.RSIDE]['button'].connect('clicked', self.toggleConnection, self.side[self.RSIDE])

        self.connect_menu()
 
        #accediendo a los controles
        #self.button = self.glade.get_object('button1')
        #self.button.connect('clicked', action)

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

    def on_window_state_event(self, widget, event):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED
        maximized = widget.get_window().get_state() & mask == mask
        self.data.set('maximized', maximized)
        return False

    def mainQuit(self, widget):

        #self.data.set('maximized', maximized)
        self.data.write()
        gtk.main_quit()

    def persist(self):
        self.data.write()

    def toggled_menu_item(self, widget, conn):
        if conn['connected'] != widget.get_active():
            self.toggleConnection(widget, conn)

    def toggleConnection(self, widget, conn):

        print 'toggleConnection'
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
            self.ping.kill()
            self.ping = None

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

    def showAbout(self, widget):
        dialog = gtk.AboutDialog()
        dialog.set_name('MySQL Diff')
        dialog.set_version('0.1 Alpha');
        dialog.set_authors(['Pablo Bangueses'])
        dialog.run()
        dialog.hide()

    #    def show_dialog(self, message, title = 'Confirm', type = gtk.MESSAGE_INFO):
    #        dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
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

    def openPreferences(self, widget):
        window = PreferencesDialog.PreferencesDialog()

    def connect_menu(self):

        self.builder.get_object('menu_file_connect1').connect('toggled', self.toggled_menu_item, self.side[self.LSIDE])
        self.builder.get_object('menu_file_connect2').connect('toggled', self.toggled_menu_item, self.side[self.RSIDE])

        self.builder.get_object('menu_file_quit').connect('activate', self.mainQuit)

        self.builder.get_object('menu_tools_preferences').connect('activate', self.openPreferences)
        self.builder.get_object('menu_tools_connections').connect('activate', self.openConnectionsEditor)

        help_help = self.builder.get_object('menu_help_help')
        help_help.connect('activate', self.presenter.open_url, 'http://bng5.net/help')
        help_reportbug = self.builder.get_object('menu_help_reportbug')
        help_reportbug.connect('activate', self.presenter.open_url, 'https://github.com/bng5/MySQLDiff/issues')
        help_translate = self.builder.get_object('menu_help_translate')
        help_translate.connect('activate', self.presenter.open_url, 'http://bng5.net/translate')

        help_about = self.builder.get_object('menu_help_about')
        help_about.connect('activate', self.showAbout)

    def schemas_combo(self, combo):
        combo.set_model(gtk.ListStore(gobject.TYPE_STRING))
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
