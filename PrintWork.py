from PyQt4 import QtCore, QtGui, QtSql
from code128 import Code128
from PIL import ImageQt
from dbConnection import db_err

font = QtGui.QFont()
font.setPointSize(18)

font_bold = QtGui.QFont()
font_bold.setPointSize(18)
font_bold.setBold(True)
font_bold.setWeight(75)

font_info = QtGui.QFont()
font_info.setPointSize(11)


class PrintWork(QtGui.QDialog):
    def __init__(self, tracking, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(3600, 2400)
        self.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.layout = QtGui.QGridLayout(self)
        self.layout.setMargin(0)
        self.layout.setColumnStretch(1, 1)

        self.top_frame = QtGui.QFrame(self)

        self.top_frame.setStyleSheet("background-color: rgb(160, 160, 160);")
        self.top_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.top_layout = QtGui.QHBoxLayout(self.top_frame)
        self.part_label = QtGui.QLabel("Part #:", self.top_frame)
        self.part_label.setFont(font)
        self.part_number = QtGui.QLabel(self.top_frame)
        self.part_number.setFont(font_bold)
        self.part_number.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.part_number.setFrameShape(QtGui.QFrame.Box)
        self.qty_label = QtGui.QLabel("Qty:", self.top_frame)
        self.qty_label.setFont(font)
        self.qty = QtGui.QLabel(self.top_frame)
        self.qty.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.qty.setFont(font_bold)
        self.qty.setFrameShape(QtGui.QFrame.Box)
        self.barcode = QtGui.QLabel(self.top_frame)
        self.barcode.setMinimumSize(QtCore.QSize(200, 50))
        self.barcode.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.barcode.setFrameShape(QtGui.QFrame.Box)
        self.barcode.setAlignment(QtCore.Qt.AlignCenter)
        self.barcode_b = QtGui.QLabel(self.top_frame)
        self.barcode_b.setMinimumSize(QtCore.QSize(200, 50))
        self.barcode_b.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.barcode_b.setFrameShape(QtGui.QFrame.Box)
        self.barcode_b.setAlignment(QtCore.Qt.AlignCenter)

        self.top_layout.addWidget(self.part_label)
        self.top_layout.addWidget(self.part_number)
        self.top_layout.addWidget(self.qty_label)
        self.top_layout.addWidget(self.qty)
        self.top_layout.addStretch(1)
        self.top_layout.addWidget(self.barcode)

        self.info_frame = QtGui.QFrame(self)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.info_frame.sizePolicy().hasHeightForWidth())
        self.info_frame.setSizePolicy(size_policy)
        self.info_frame.setMinimumSize(QtCore.QSize(250, 0))
        self.info_frame.setMaximumSize(QtCore.QSize(250, 1200))
        self.info_frame.setFont(font_info)
        self.info_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QtGui.QFrame.Raised)

        self.info_layout = QtGui.QGridLayout(self.info_frame)

        self.description_label = QtGui.QLabel("Desc.", self.info_frame)
        self.description = QtGui.QLineEdit(self.info_frame)
        self.material_label = QtGui.QLabel("Mat.", self.info_frame)
        self.material = QtGui.QLineEdit(self.info_frame)
        self.routing_label = QtGui.QLabel("Rout.", self.info_frame)
        self.routing = QtGui.QLineEdit(self.info_frame)
        self.destination_label = QtGui.QLabel("Dest.", self.info_frame)
        self.destination = QtGui.QLineEdit(self.info_frame)
        self.blank_label = QtGui.QLabel("Blank", self.info_frame)
        self.blank = QtGui.QLineEdit(self.info_frame)
        self.clamp_label = QtGui.QLabel("Clamp", self.info_frame)
        self.clamp = QtGui.QLineEdit(self.info_frame)
        self.notes_label = QtGui.QLabel("Notes", self.info_frame)
        self.notes = QtGui.QPlainTextEdit(self.info_frame)
        self.notes.setMaximumSize(QtCore.QSize(600, 75))

        self.machining_info_layout = QtGui.QGridLayout()
        self.bar_label = QtGui.QLabel("Bar Pull", self.info_frame)
        self.bar = QtGui.QLineEdit(self.info_frame)
        self.pos_stop_label = QtGui.QLabel("Pos. Stop", self.info_frame)
        self.pos_stop = QtGui.QLineEdit(self.info_frame)
        self.square_label = QtGui.QLabel("Square Set", self.info_frame)
        self.square = QtGui.QLineEdit(self.info_frame)

        self.machining_info_layout.addWidget(self.bar_label, 0, 0, 1, 1)
        self.machining_info_layout.addWidget(self.bar, 1, 0, 1, 1)
        self.machining_info_layout.addWidget(self.pos_stop_label, 0, 1, 1, 1)
        self.machining_info_layout.addWidget(self.pos_stop, 1, 1, 1, 1)
        self.machining_info_layout.addWidget(self.square_label, 0, 2, 1, 1)
        self.machining_info_layout.addWidget(self.square, 1, 2, 1, 1)

        self.time_layout = QtGui.QGridLayout()
        self.load_label = QtGui.QLabel("(Un)Load", self.info_frame)
        self.load = QtGui.QLineEdit(self.info_frame)
        self.run_label = QtGui.QLabel("Run", self.info_frame)
        self.run = QtGui.QLineEdit(self.info_frame)
        self.setup_label = QtGui.QLabel("Setup", self.info_frame)
        self.setup = QtGui.QLineEdit(self.info_frame)

        self.time_layout.addWidget(self.load_label, 0, 0, 1, 1)
        self.time_layout.addWidget(self.load, 1, 0, 1, 1)
        self.time_layout.addWidget(self.run_label, 0, 1, 1, 1)
        self.time_layout.addWidget(self.run, 1, 1, 1, 1)
        self.time_layout.addWidget(self.setup_label, 0, 2, 1, 1)
        self.time_layout.addWidget(self.setup, 1, 2, 1, 1)

        self.program = QtGui.QLabel(self.info_frame)
        info_spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.setup_pix = QtGui.QLabel(self.info_frame)

        self.info_layout.addWidget(self.description_label, 0, 0, 1, 1)
        self.info_layout.addWidget(self.description, 0, 1, 1, 1)
        self.info_layout.addWidget(self.material_label, 1, 0, 1, 1)
        self.info_layout.addWidget(self.material, 1, 1, 1, 1)
        self.info_layout.addWidget(self.routing_label, 2, 0, 1, 1)
        self.info_layout.addWidget(self.routing, 2, 1, 1, 1)
        self.info_layout.addWidget(self.destination_label, 3, 0, 1, 1)
        self.info_layout.addWidget(self.destination, 3, 1, 1, 1)
        self.info_layout.addWidget(self.blank_label, 4, 0, 1, 1)
        self.info_layout.addWidget(self.blank, 4, 1, 1, 1)
        self.info_layout.addWidget(self.clamp_label, 5, 0, 1, 1)
        self.info_layout.addWidget(self.clamp, 5, 1, 1, 1)
        self.info_layout.addWidget(self.notes_label, 6, 0, 1, 1)
        self.info_layout.addWidget(self.notes, 6, 1, 1, 1)
        self.info_layout.addLayout(self.machining_info_layout, 7, 0, 1, 2)
        self.info_layout.addLayout(self.time_layout, 8, 0, 1, 2)
        self.info_layout.addWidget(self.program, 9, 0, 1, 2)
        self.info_layout.addItem(info_spacer, 10, 0, 1, 1)
        self.info_layout.addWidget(self.setup_pix, 11, 0, 1, 2)

        self.print_holder = QtGui.QLabel(self)
        self.print_holder.setMinimumSize(QtCore.QSize(500, 500))
        self.print_holder.setAlignment(QtCore.Qt.AlignCenter)

        self.bottom_frame = QtGui.QFrame(self)
        self.bottom_frame.setStyleSheet("background-color: rgb(160, 160, 160);")
        self.bottom_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.bottom_layout = QtGui.QHBoxLayout(self.bottom_frame)
        self.bottom_layout.addWidget(self.barcode_b)
        self.bottom_layout.addStretch(1)

        self.layout.addWidget(self.top_frame, 0, 0, 1, 2)
        self.layout.addWidget(self.info_frame, 1, 0, 1, 1)
        self.layout.addWidget(self.print_holder, 1, 1, 1, 1)
        self.layout.addWidget(self.bottom_frame, 2, 0, 1, 2)

        part, qty, ok = self.get_part_qty(tracking)
        if not ok:
            text = "There was an issue finding the part related to {0}".format(tracking)
            QtGui.QMessageBox.critical(self, "Part Error", text)
        else:
            self.print_holder.resizeEvent = self.load_print
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
                    self.part_number.setText(part_num)
                    self.qty.setText(str(qty))
                    self.description.setText(desc)
                    self.material.setText(mat)
                    self.routing.setText(rout)
                    self.destination.setText(dest)
                    self.notes.setPlainText(notes)
                    self.program.setText(prog)
                    self.clamp.setText(clamp)
                    self.bar.setText(bar_pull)
                    self.square.setText(square)
                    self.pos_stop.setText(pos_stop)
                    self.run.setText(run)
                    self.load.setText(load)
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
        self.barcode_b.setPixmap(barcode_pix)

    def load_print(self, event):
        """
        Try to load a print for the current part.
        See 'readSettings' for 'self.prints'.
        An error message is raised if the image doesn't exist.
        """
        print_file = '{0}/{1}.jpg'.format(self.prints, self.part_number.text())
        print_pix = QtGui.QPixmap(print_file)
        if print_pix.isNull():
            self.print_holder.clear()
        else:
            self.print_holder.setPixmap(print_pix.scaled(self.print_holder.size(), 1, 1))

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
