from PyQt4 import QtCore, QtGui, QtSql, uic
from dbConnection import db_err


class Material(QtGui.QDialog):
    def __init__(self, parent=None):
        def connections():
            self.filter.textEdited.connect(self.filter_)

        QtGui.QDialog.__init__(self, parent)
        uic.loadUi('ui/material.ui', self)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        connections()
        self.get_data()
        QtGui.QApplication.restoreOverrideCursor()
        
    def get_data(self):
        mat_mod = QtSql.QSqlTableModel()
        mat_mod.setTable('`material`')
        mat_mod.setEditStrategy(0)
        if mat_mod.select():
            self.materialTable.setModel(mat_mod)
            self.materialTable.resizeColumnToContents(1)
        else:
            db_err(mat_mod)
    
    def filter_(self, text):
        self.materialTable.model().setFilter("material like '{0}%'".format(text))
        self.materialTable.model().select()
