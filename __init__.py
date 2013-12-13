import sys
import time
from PyQt4 import QtCore, QtGui, uic
from Orders import Orders
from Parts import Parts
from Material import Material
from Schedule import Schedule
from Barcode import Barcode
from dbConnection import default_connection
from functions import partnum_to_partid, restore_cursor


class Main(QtGui.QMainWindow):
    """
    Main script for the machining system.
    Opens the main window with the mdiArea and menu.
    This script should only be used for opening new sudwindows.
    
    If a connection to the database can not be made, the application 
    warns and then closes.
    """
    def __init__(self, parent=None):
        def connections():
            self.ordersBut.clicked.connect(self.show_orders)
            self.partsBut.clicked.connect(self.show_parts)
            self.materialBut.clicked.connect(self.show_material)
            self.scheduleBut.clicked.connect(self.show_schedule)
            self.barcodeBut.clicked.connect(self.show_barcode)
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi('ui/main.ui', self)
        self.read_settings()
        connections()
    
    def new_subwindow(self, mod):
        """
        Function creating new subWindows
        """
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        sub = self.mdiArea.addSubWindow(mod())
        sub.showMaximized()
        restore_cursor()
        return sub
        
####SubWindow Calls
    def show_orders(self, a=None):
        orders = self.new_subwindow(Orders)
        orders_widget = orders.widget()
        orders_widget.setWindowIcon(QtGui.QIcon('ui/orders.png'))
        orders_widget.goto_part.connect(self.goto_parts)
        return orders
        
    def show_parts(self, a=None):
        parts = self.new_subwindow(Parts)
        parts.widget().setWindowIcon(QtGui.QIcon('ui/parts.png'))
        return parts

    def show_schedule(self, a=None):
        schedule = self.new_subwindow(Schedule)
        schedule_widget = schedule.widget()
        schedule_widget.goto_part.connect(self.goto_parts)

    def show_material(self, a=None):
        material = Material()
        material.show()
        screen_center = self.geometry().center()
        widget_center = material.rect().center()
        material.move(screen_center-widget_center)

    def show_barcode(self, a=None):
        barcode = Barcode(self)
        barcode.show()
        screen_center = self.geometry().center()
        widget_center = barcode.rect().center()
        barcode.move(screen_center-widget_center)
####

    def goto_parts(self, part):
        """
        Opens the parts form and goes to part.
        part should be a part number not a part id.
        """
        part_id = partnum_to_partid(part)
        parts = self.show_parts()
        parts.widget().load_data(part=part_id)
    
    def closeEvent(self,  event):
        """
        Simply saving the size and positions settings so they can
        be restored next time the application is opened.
        """
        self.write_settings()

####Settings Block
    def read_settings(self):
        settings = QtCore.QSettings("Riverview", "Machining")
        settings.beginGroup("Main")
        self.resize(settings.value("size", QtCore.QSize(640, 480)).toSize())
        self.move(settings.value("pos", QtCore.QPoint(150, 200)).toPoint())
        settings.endGroup()
        
    def write_settings(self):
        settings = QtCore.QSettings("Riverview", "Machining")
        settings.beginGroup("Main")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()
####


def main():
    def update_splash(text):
        splash.showMessage(text)
        app.processEvents()

    app = QtGui.QApplication(sys.argv)
    splash_img = QtGui.QPixmap("splash.png")
    splash = QtGui.QSplashScreen(splash_img, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    time.sleep(.001)
    update_splash("Establishing Connection...")
    if not default_connection():
        QtGui.QMessageBox.critical(None, "No Connection!", "The database connection could not be established.")
        sys.exit(1)
    update_splash("Loading GUI...")
    myapp = Main()
    myapp.show()
    update_splash("GUI Loaded...")
    splash.finish(myapp)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
