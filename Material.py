from PyQt4 import QtCore, QtGui, QtSql
from dbConnection import db_err


class Material(QtGui.QDialog):
    def __init__(self, parent=None):
        def connections():
            self.filter.textEdited.connect(self.filter_)

        QtGui.QDialog.__init__(self, parent)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(650, 672)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowIcon(QtGui.QIcon(":/icons/material.png"))

        self.material_table = QtGui.QTableView(self)
        self.filter = QtGui.QLineEdit(self)
        spacer = QtGui.QSpacerItem(191, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.layout = QtGui.QGridLayout(self)
        self.layout.addWidget(self.material_table, 0, 0, 1, 2)
        self.layout.addWidget(self.filter, 1, 1, 1, 1)
        self.layout.addItem(spacer, 1, 0, 1, 1)

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
            self.material_table.setModel(mat_mod)
            self.material_table.resizeColumnToContents(1)
        else:
            db_err(mat_mod)
    
    def filter_(self, text):
        self.material_table.model().setFilter("material like '{0}%'".format(text))
        self.material_table.model().select()
