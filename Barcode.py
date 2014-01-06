from PyQt4 import QtCore, QtGui
from dbConnection import write_connection, start_transaction, commit_transaction, rollback_transaction
from query import query


class Barcode(QtGui.QDialog):
    def __init__(self, parent=None):
        def connections():
            self.track.returnPressed.connect(self.update)

        QtGui.QDialog.__init__(self, parent)
        self.resize(287, 90)
        self.setWindowIcon(QtGui.QIcon(":/icons/barcode.png"))

        self.status = QtGui.QLineEdit(self)
        self.status.setPlaceholderText("status...")
        self.track = QtGui.QLineEdit(self)
        self.track.setPlaceholderText("tracking...")

        self.layout = QtGui.QGridLayout(self)
        self.layout.addWidget(self.status, 0, 0, 1, 1)
        self.layout.addWidget(self.track, 1, 0, 1, 1)

        self.setModal(True)

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        connections()
        self.completer()
        self.dbw, ok = write_connection()
        QtGui.QApplication.restoreOverrideCursor()
        if not ok:
            self.done(0)

    def update(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        track = self.track.text()
        status = self.status.text()
        fin = '0'
        if status != "" and track != "":
            qry = query("get_qty", [track])
            if qry:
                if qry.first():
                    qty = int(qry.value(0).toString())
                else:
                    return
            else:
                return
            qty, ok = QtGui.QInputDialog.getInt(self, "How many good parts did you make?",
                                                "How many good parts did you make?", qty)
            if ok:
                if start_transaction("write"):
                    qry = query("new_status", [status, track, fin, qty], "write")
                    if not qry:
                        rollback_transaction("write")
                        return

                qry = query("get_machine_id", [status])
                if qry:
                    if qry.first():
                        mach = qry.value(0).toString()
                        qry = query("update_schedule", [mach, track])
                        if not qry:
                            rollback_transaction("write")
                else:
                    rollback_transaction("write")
                if not commit_transaction("write"):
                    rollback_transaction("write")
        self.track.setText("")
        self.track.setFocus()
        QtGui.QApplication.restoreOverrideCursor()

    def completer(self):
        qry = query("get_machines")
        if qry:
            status = ['Delivery', 'Lost', 'Shipping']
            while qry.next():
                status.append(qry.value(0).toString())
            comp = QtGui.QCompleter(status)
            comp.setCaseSensitivity(0)
            self.status.setCompleter(comp)