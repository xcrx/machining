from PyQt4 import QtCore, QtGui, QtSql, uic
from dbConnection import db_err


class Schedule(QtGui.QWidget):
    goto_part = QtCore.pyqtSignal([str])

    def __init__(self, parent=None):
        def connections():
            self.up.clicked.connect(self.up_)
            self.down.clicked.connect(self.down_)
            self.remove.clicked.connect(self.remove_)
            self.add.clicked.connect(self.add_)

        QtGui.QWidget.__init__(self, parent)
        uic.loadUi('ui/schedule.ui', self)
        connections()
        self.generate_schedules()
        
    def generate_schedules(self):
        sch_qry = QtSql.QSqlQuery()
        if sch_qry.exec_("Select Status_Description from vScheduleStatus group by Status_Description"):
            names = []
            while sch_qry.next():
                names.append(sch_qry.value(0).toString())
            for name in names:
                self.new_tab(name)
        else:
            db_err(sch_qry)
    
    def new_tab(self, name):
        sch_qry = QtSql.QSqlQuery()
        data = "Select * from vSchedule where `Status` = '{0}'".format(name)
        if sch_qry.exec_(data):
            try:
                sch_qry.first()
                mod = QtSql.QSqlQueryModel()
                mod.setQuery(sch_qry)
                table = QtGui.QTableView()
                table.setModel(mod)
                table.resizeColumnsToContents()
                table.id = Schedule
                table.doubleClicked.connect(self.goto_part_)
                self.tabs.addTab(table, name)
            except Exception as e:
                print e
        else:
            db_err(sch_qry)
    
    def goto_part_(self, index):
        row = index.row()
        mod = index.model()
        part = mod.data(mod.index(row, 0)).toString()
        self.goto_part.emit(part)
    
    def up_(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            widget = self.tabs.currentWidget()
            index = widget.currentIndex()
            mod = index.model()
            row = index.row()
            track = mod.data(mod.index(row, 8)).toString()
            mach = mod.data(mod.index(row, 9)).toString()
            pos = mod.data(mod.index(row, 0)).toString()
            qry = QtSql.QSqlQuery()
            data = "Update schedule set pos=IF(pos>0,pos-1,0) where trackingid={0} and machine={1}".format(track, mach)
            if qry.exec_(data):
                r_qry = mod.query()
                if r_qry.exec_():
                    mod.setQuery(r_qry)
                    r = mod.rowCount()
                    row = 0
                    while row < r:
                        if mod.data(mod.index(row, 8)).toString() == track:
                            widget.selectRow(row)
                            break
                        row += 1
                else:
                    db_err(r_qry)
            else:
                db_err(qry)
        except Exception as e:
            print e
        QtGui.QApplication.restoreOverrideCursor()
        
    def down_(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            widget = self.tabs.currentWidget()
            index = widget.currentIndex()
            mod = index.model()
            row = index.row()
            track = mod.data(mod.index(row, 8)).toString()
            mach = mod.data(mod.index(row, 9)).toString()
            qry = QtSql.QSqlQuery()
            data = "Update schedule set pos=pos+1 where trackingid={0} and machine={1}".format(track, mach)
            if qry.exec_(data):
                r_qry = mod.query()
                if r_qry.exec_():
                    mod.setQuery(r_qry)
                    r = mod.rowCount()
                    row = 0
                    while row < r:
                        if mod.data(mod.index(row, 8)).toString() == track:
                            widget.selectRow(row)
                            break
                        row += 1
                else:
                    db_err(r_qry)
            else:
                db_err(qry)
        except Exception as e:
            print e
        QtGui.QApplication.restoreOverrideCursor()
        
    def remove_(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            widget = self.tabs.currentWidget()
            index = widget.currentIndex()
            mod = index.model()
            row = index.row()
            track = mod.data(mod.index(row, 8)).toString()
            mach = mod.data(mod.index(row, 9)).toString()
            qry = QtSql.QSqlQuery()
            data = "delete from schedule where trackingid={0} and machine={1}".format(track, mach)
            if qry.exec_(data):
                r_qry = mod.query()
                if r_qry.exec_():
                    mod.setQuery(r_qry)
                else:
                    db_err(r_qry)
            else:
                db_err(qry)
        except Exception as e:
            print e
        QtGui.QApplication.restoreOverrideCursor()
    
    def add_(self):
        track, ok = QtGui.QInputDialog.getInt(self, "Scan Barcode", "")
        if ok:
            widget = self.tabs.currentWidget()
            index = widget.currentIndex()
            mod = index.model()
            mach = widget.id
            qry = QtSql.QSqlQuery()
            data = ("Replace into schedule set trackingId={0}, machine={1}, pos=(select max(pos)+1 "
                    "from schedule as a where machine={1})").format(track, mach)
            if qry.exec_(data):
                r_qry = mod.query()
                if r_qry.exec_():
                    mod.setQuery(r_qry)
                    r = mod.rowCount()
                    row = 0
                    while row < r:
                        if mod.data(mod.index(row, 8)).toString() == track:
                            widget.selectRow(row)
                            break
                        row += 1
                else:
                    db_err(r_qry)
            else:
                db_err(qry)
