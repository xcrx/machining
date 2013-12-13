from PyQt4 import QtCore, QtGui, QtSql, uic
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
            self.activeTable.entered.connect(self.load_print)
            self.waitingTable.entered.connect(self.load_print)
            self.setupTable.entered.connect(self.load_print)
            self.setupTable.doubleClicked.connect(self.go_to_part)
            self.activeTable.doubleClicked.connect(self.go_to_part)
            self.waitingTable.doubleClicked.connect(self.go_to_part)
            self.inProcessTable.doubleClicked.connect(self.go_to_part)
            self.workOrder.clicked.connect(self.new_work_order)
            self.shortcuts()

        QtGui.QWidget.__init__(self, parent)
        uic.loadUi('ui/currentOrders.ui', self)
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
            self.activeTable.setModel(active_mod)
            self.activeTable.resizeColumnsToContents()
            return True
        else:
            return False

    def load_setup_orders(self):
        qry = query("setup_orders")
        if qry:
            setup_mod = QtSql.QSqlQueryModel()
            setup_mod.setQuery(qry)
            self.setupTable.setModel(setup_mod)
            self.setupTable.resizeColumnsToContents()
            return True
        else:
            return False

    def load_material_orders(self):
        qry = query("material_orders")
        if qry:
            material_mod = QtSql.QSqlQueryModel()
            material_mod.setQuery(qry)
            self.waitingTable.setModel(material_mod)
            self.waitingTable.resizeColumnsToContents()
            return True
        else:
            return False

    def load_in_process(self):
        qry = query("in_process_orders")
        if qry:
            in_process_mod = QtSql.QSqlQueryModel()
            in_process_mod.setQuery(qry)
            self.inProcessTable.setModel(in_process_mod)
            self.inProcessTable.resizeColumnsToContents()
            return True
        else:
            return False

    def filter_orders(self, text):
        mod = self.activeTable.model()
        i = 0
        while i < mod.rowCount():
            e = 0
            x = True
            while e < mod.columnCount():
                if text.toLower() in mod.data(mod.index(i, e)).toString().toLower():
                    x = False
                e += 1
            self.activeTable.setRowHidden(i, x)
            i += 1

    def search_orders(self):
        mod = self.activeTable.model()
        text = self.search.text()
        i = self.activeTable.currentIndex().row()+1
        found = False
        while i < mod.rowCount():
            e = 0
            x = False
            while e < mod.columnCount():
                if text.toLower() in mod.data(mod.index(i, e)).toString().toLower():
                    x = True
                e += 1
            if x:
                self.activeTable.selectRow(i)
                found = True
                break
            i += 1
        if not found:
            QtGui.QMessageBox.information(self, "Not Found", "'{0}' not found!".format(text))
            self.activeTable.selectRow(0)

    def load_print(self, index):
        row = index.row()
        col = index.column()
        file_name = index.model().data(index.model().index(row, 0)).toString()
        if index.model() == self.activeTable.model():
            table = self.activeTable
        elif index.model() == self.waitingTable.model():
            table = self.waitingTable
        elif index.model() == self.setupTable.model():
            table = self.setupTable
        else:
            return
        if col == 0:
            table.setToolTip('<img src="{0}/{1}.jpg" width="480" height="320"/>'.format(self.prints, file_name))
        else:
            table.setToolTip("")

    def new_work_order(self):
        index = self.activeTable.currentIndex()
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