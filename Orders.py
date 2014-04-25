from PyQt4 import QtCore, QtGui, QtSql
from PrintWork import PrintWork
from dbConnection import write_connection, db_err
from workOrder import save_work_order
from query import query


class Orders(QtGui.QWidget):
    goto_part = QtCore.pyqtSignal([str])

    def __init__(self, parent=None):
        def connections():
            self.filter.textChanged.connect(self.filter_orders)
            self.search.returnPressed.connect(self.search_orders)
            self.active_table.entered.connect(self.load_print)
            self.waiting_table.entered.connect(self.load_print)
            self.setup_table.entered.connect(self.load_print)
            self.setup_table.doubleClicked.connect(self.go_to_part)
            self.active_table.doubleClicked.connect(self.go_to_part)
            self.waiting_table.doubleClicked.connect(self.go_to_part)
            self.in_process_table.doubleClicked.connect(self.go_to_part)
            self.work_order.clicked.connect(self.new_work_order)
            self.shortcuts()

        QtGui.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon(":/icons/orders.png"))
        self.layout = QtGui.QGridLayout(self)
        self.work_order = QtGui.QPushButton("Create Work Order", self)
        self.search = QtGui.QLineEdit(self)
        self.search.setPlaceholderText("Search...")
        self.filter = QtGui.QLineEdit(self)
        self.filter.setPlaceholderText("Filter...")
        self.tab_widget = QtGui.QTabWidget(self)
        self.tab_widget.setMouseTracking(True)

        self.layout.addWidget(self.work_order, 0, 0, 1, 1)
        self.layout.addWidget(self.search, 0, 1, 1, 1)
        self.layout.addWidget(self.filter, 0, 2, 1, 1)
        self.layout.setColumnStretch(3, 1)
        self.layout.addWidget(self.tab_widget, 1, 0, 1, 4)

        self.active_table = QtGui.QTableView(self.tab_widget)
        self.active_table.setMouseTracking(True)
        self.in_process_table = QtGui.QTableView(self.tab_widget)
        self.in_process_table.setMouseTracking(True)
        self.waiting_table = QtGui.QTableView(self.tab_widget)
        self.waiting_table.setMouseTracking(True)
        self.setup_table = QtGui.QTableView(self.tab_widget)
        self.setup_table.setMouseTracking(True)

        self.tab_widget.addTab(self.active_table, "Active Orders")
        self.tab_widget.addTab(self.in_process_table, "In Process")
        self.tab_widget.addTab(self.waiting_table, "Waiting on Material")
        self.tab_widget.addTab(self.setup_table, "No Setup")

        self.read_settings()
        connections()
        self.load_orders()

    def load_orders(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.load_available_orders()
        self.load_in_process()
        self.load_setup_orders()
        self.load_material_orders()
        QtGui.QApplication.restoreOverrideCursor()

    def load_available_orders(self):
        qry = query("active_orders")
        if qry:
            active_mod = QtSql.QSqlQueryModel()
            active_mod.setQuery(qry)
            self.active_table.setModel(active_mod)
            self.active_table.resizeColumnsToContents()
            return True
        else:
            return False

    def load_setup_orders(self):
        qry = query("setup_orders")
        if qry:
            setup_mod = QtSql.QSqlQueryModel()
            setup_mod.setQuery(qry)
            self.setup_table.setModel(setup_mod)
            self.setup_table.resizeColumnsToContents()
            return True
        else:
            return False

    def load_material_orders(self):
        qry = query("material_orders")
        if qry:
            material_mod = QtSql.QSqlQueryModel()
            material_mod.setQuery(qry)
            self.waiting_table.setModel(material_mod)
            self.waiting_table.resizeColumnsToContents()
            return True
        else:
            return False

    def load_in_process(self):
        qry = query("in_process_orders")
        if qry:
            in_process_mod = QtSql.QSqlQueryModel()
            in_process_mod.setQuery(qry)
            self.in_process_table.setModel(in_process_mod)
            self.in_process_table.resizeColumnsToContents()
            return True
        else:
            return False

    def filter_orders(self, text):
        mod = self.active_table.model()
        i = 0
        while i < mod.rowCount():
            e = 0
            x = True
            while e < mod.columnCount():
                if text.toLower() in mod.data(mod.index(i, e)).toString().toLower():
                    x = False
                e += 1
            self.active_table.setRowHidden(i, x)
            i += 1

    def search_orders(self):
        mod = self.active_table.model()
        text = self.search.text()
        i = self.active_table.currentIndex().row()+1
        found = False
        while i < mod.rowCount():
            e = 0
            x = False
            while e < mod.columnCount():
                if text.toLower() in mod.data(mod.index(i, e)).toString().toLower():
                    x = True
                e += 1
            if x:
                self.active_table.selectRow(i)
                found = True
                break
            i += 1
        if not found:
            QtGui.QMessageBox.information(self, "Not Found", "'{0}' not found!".format(text))
            self.active_table.selectRow(0)

    def load_print(self, index):
        row = index.row()
        col = index.column()
        file_name = index.model().data(index.model().index(row, 0)).toString()
        if index.model() == self.active_table.model():
            table = self.active_table
        elif index.model() == self.waiting_table.model():
            table = self.waiting_table
        elif index.model() == self.setup_table.model():
            table = self.setup_table
        else:
            return
        if col == 0:
            table.setToolTip('<img src="{0}/{1}.jpg" width="480" height="320"/>'.format(self.prints, file_name))
        else:
            table.setToolTip("Not Working")

    def new_work_order(self):
        index = self.active_table.currentIndex()
        row = index.row()
        mod = index.model()
        self.part = mod.data(mod.index(row, 9)).toString()
        self.part_num = mod.data(mod.index(row, 0)).toString()
        i, a = mod.data(mod.index(row, 2)).toInt()
        e, a = mod.data(mod.index(row, 3)).toInt()
        qty = i-e
        text = "How many of {0} for this work order?".format(self.part_num)
        self.qty, ok = QtGui.QInputDialog.getInt(self, "Order Quantity", text, qty)
        if ok:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.tracking, ok = save_work_order(self.part, self.qty)
            if ok:
                print_ = QtGui.QPrintPreviewDialog()
                print_.paintRequested.connect(self.print_preview)
                print_.exec_()
        self.load_orders()
        QtGui.QApplication.restoreOverrideCursor()

    def print_preview(self, printer):
        printer.setOrientation(1)
        printer.setPaperSize(printer.PageSize(2))
        printer.setPageSize(printer.PageSize(2))
        printer.setPageMargins(.25, .25, .25, .25, 2)
        printer.newPage()
        self.print_work = PrintWork(self.tracking)
        self.print_work.setGeometry(printer.pageRect())
        self.print_work.render(printer)

    def go_to_part(self, index):
        row = index.row()
        mod = index.model()
        part = mod.data(mod.index(row, 0)).toString()
        self.goto_part.emit(part)

    def shortcuts(self):
        self.refresh = QtGui.QShortcut(self)
        self.refresh.setKey(QtGui.QKeySequence("F5"))
        self.refresh.activated.connect(self.load_orders)

####Settings Block
    def read_settings(self):
        settings = QtCore.QSettings("Riverview", "Machining")
        settings.beginGroup("Main")
        self.prints = settings.value("prints", None).toString()
        settings.endGroup()
        if self.prints == "":
            self.prints = QtGui.QFileDialog.getExistingDirectory(self, "Prints Location")
            self.write_settings(self.prints)

    def write_settings(self, prints):
        settings = QtCore.QSettings("Riverview", "Machining")
        settings.beginGroup("Main")
        settings.setValue("prints", prints)
        settings.endGroup()
####