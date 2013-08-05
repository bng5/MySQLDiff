import gtk
import constants

def about():
    dialog = gtk.AboutDialog()
    dialog.set_program_name('MySQL Diff')
    dialog.set_version(constants.VERSION+' Alpha');
    dialog.set_authors(['Pablo Bangueses'])
    dialog.set_website('http://bng5.net/mysqldiff')
    dialog.run()
    dialog.hide()


