import sys
import time
from PyQt4 import QtCore, QtGui
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
    This script should only be used for opening new sud-windows.
    
    If a connection to the database can not be made, the application 
    warns and then closes.
    """
    def __init__(self):
        def connections():
            self.orders_button.clicked.connect(self.show_orders)
            self.parts_button.clicked.connect(self.show_parts)
            self.material_button.clicked.connect(self.show_material)
            self.schedule_button.clicked.connect(self.show_schedule)
            self.barcode_button.clicked.connect(self.show_barcode)

        QtGui.QMainWindow.__init__(self)
        self.resize(800, 600)
        self.setWindowTitle("Machining")
        self.setWindowIcon(QtGui.QIcon("ui//main.png"))

        self.central_widget = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.central_widget)

        self.frame = QtGui.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(0, 35))
        self.frame.setMaximumSize(QtCore.QSize(2000, 40))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)

        self.orders_button = QtGui.QPushButton(QtGui.QIcon("ui/orders.png"), "Orders", self.frame)
        self.schedule_button = QtGui.QPushButton(QtGui.QIcon("ui/schedule.png"), "Schedule", self.frame)
        self.parts_button = QtGui.QPushButton(QtGui.QIcon("ui/parts.png"), "Parts", self.frame)
        self.material_button = QtGui.QPushButton(QtGui.QIcon("ui/material.png"), "Material", self.frame)
        self.barcode_button = QtGui.QPushButton(QtGui.QIcon("ui/barcode.png"), "Barcode", self.frame)

        self.button_layout = QtGui.QHBoxLayout(self.frame)
        self.button_layout.setContentsMargins(9, 1, 9, 1)
        self.button_layout.addWidget(self.orders_button)
        self.button_layout.addWidget(self.schedule_button)
        self.button_layout.addWidget(self.parts_button)
        self.button_layout.addWidget(self.material_button)
        self.button_layout.addWidget(self.barcode_button)
        self.button_layout.addStretch(1)
        self.frame.setLayout(self.button_layout)

        self.mdi_area = QtGui.QMdiArea(self)
        self.mdi_area.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdi_area.setTabsClosable(True)
        self.mdi_area.setTabsMovable(True)
        self.mdi_area.setBackground(QtGui.QBrush(QtGui.QColor(155, 155, 155), QtCore.Qt.Dense4Pattern))

        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.mdi_area)
        self.setCentralWidget(self.central_widget)

        self.read_settings()
        connections()
    
    def new_subwindow(self, mod):
        """
        Function creating new subWindows
        """
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        sub = self.mdi_area.addSubWindow(mod())
        sub.showMaximized()
        restore_cursor()
        return sub
        
####SubWindow Calls
    def show_orders(self):
        orders = self.new_subwindow(Orders)
        orders_widget = orders.widget()
        orders_widget.setWindowIcon(QtGui.QIcon('ui/orders.png'))
        orders_widget.goto_part.connect(self.go_to_parts)
        return orders
        
    def show_parts(self):
        parts = self.new_subwindow(Parts)
        parts.widget().setWindowIcon(QtGui.QIcon('ui/parts.png'))
        return parts

    def show_schedule(self):
        schedule = self.new_subwindow(Schedule)
        schedule_widget = schedule.widget()
        schedule_widget.goto_part.connect(self.go_to_parts)

    def show_material(self):
        material = Material(self)
        material.show()
        screen_center = self.geometry().center()
        widget_center = material.rect().center()
        material.move(screen_center-widget_center)

    def show_barcode(self):
        barcode = Barcode(self)
        barcode.show()
        screen_center = self.geometry().center()
        widget_center = barcode.rect().center()
        barcode.move(screen_center-widget_center)
####

    def go_to_parts(self, part):
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
    my_app = Main()
    my_app.show()
    update_splash("GUI Loaded...")
    splash.finish(my_app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
