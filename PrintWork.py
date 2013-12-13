from PyQt4 import QtCore, QtGui, QtSql, uic
from code128 import Code128
from PIL import ImageQt
from dbConnection import db_err


class PrintWork(QtGui.QDialog):
    def __init__(self, tracking, parent=None):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi('ui/printWork.ui', self)
        part, qty, ok = self.get_part_qty(tracking)
        if not ok:
            text = "There was an issue finding the part related to {0}".format(tracking)
            QtGui.QMessageBox.critical(self, "Part Error", text)
        else:
            self.printHolder.resizeEvent = self.load_print
            self.read_settings()
            qry = QtSql.QSqlQuery()
            if qry.exec_("select * from parts where partId = {0}".format(part)):
                if qry.first():
                    part_num = qry.value(0).toString()
                    desc = qry.value(1).toString()
                    mat = qry.value(2).toString()
                    rout = qry.value(4).toString()
                    dest = qry.value(5).toString()
                    notes = qry.value(7).toString()
                    prog = qry.value(8).toString()
                    clamp = qry.value(9).toString()
                    bar_pull = qry.value(10).toString()
                    square = qry.value(11).toString()
                    pos_stop = qry.value(12).toString()
                    run = qry.value(13).toString()
                    load = qry.value(14).toString()
                    setup = qry.value(15).toString()
                    blank = qry.value(16).toString()
                    barcode = str(tracking)
                    self.partNum.setText(part_num)
                    self.qty.setText(str(qty))
                    self.description.setText(desc)
                    self.material.setText(mat)
                    self.routing.setText(rout)
                    self.dest.setText(dest)
                    self.notes.setPlainText(notes)
                    self.program.setText(prog)
                    self.clamp.setText(clamp)
                    self.bar.setText(bar_pull)
                    self.square.setText(square)
                    self.posStop.setText(pos_stop)
                    self.run.setText(run)
                    self.unload.setText(load)
                    self.setup.setText(setup)
                    self.blank.setText(blank)
                    self.set_barcodes(barcode)
                    self.load_print(part_num)
                    QtGui.QApplication.restoreOverrideCursor()
                else:
                    QtGui.QMessageBox.critical(self, "Part Not Found", "We Couldn't find that part...")
            else:
                db_err(qry)

    def set_barcodes(self, code):
        img = Code128().get_image(code)
        barcode_image = ImageQt.ImageQt(img.convert('RGBA'))
        barcode_pix = QtGui.QPixmap.fromImage(barcode_image).scaled(200, 50, 1, 1)
        self.barcode.setPixmap(barcode_pix)
        self.barcode2.setPixmap(barcode_pix)

    def load_print(self, event):
        """
        Try to load a print for the current part.
        See 'readSettings' for 'self.prints'.
        An error message is raised if the image doesn't exist.
        """
        print_file = '{0}/{1}.jpg'.format(self.prints, self.partNum.text())
        print_pix = QtGui.QPixmap(print_file)
        if print_pix.isNull():
            self.printHolder.clear()
        else:
            self.printHolder.setPixmap(print_pix.scaled(self.printHolder.size(), 1, 1))

    def get_part_qty(self, track):
        qry = QtSql.QSqlQuery()
        data = "Select Part_ID, Qty from inventorysystem.Work_Details_tbl where Tracking_num = {0}".format(track)
        if qry.exec_(data):
            if qry.first():
                part = qry.value(0).toString()
                qty = qry.value(1).toString()
                return part, qty, True
            else:
                return None, None, False
        else:
            db_err(qry)
            return None, None, False

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
