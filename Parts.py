"""
Form for view and editing parts
"""
from PyQt4 import QtCore, QtGui, QtSql
from dbConnection import write_connection, db_err
from PrintWork import PrintWork
from workOrder import save_work_order


def prepare_string(string):
    string = string.replace('"', '\\"')
    string = string.replace("'", "\\'")
    string = string.toUtf8()
    return string


def set_max(widgets, size):
    for widget in widgets:
        widget.setMaximumSize(QtCore.QSize(600, size))
    

class Parts(QtGui.QWidget):
    def __init__(self, parent=None):
        def connections():
            self.next.clicked.connect(self.next_)
            self.previous.clicked.connect(self.previous_)
            self.printHolder.mousePressEvent = self.expand_print
            self.printHolder.resizeEvent = self.load_print
            self.setupPic.resizeEvent = self.set_setup
            self.save.clicked.connect(self.save_)
            self.addTooling.clicked.connect(self.add_tooling)
            self.printHolder.wheelEvent = self.wheel_navi
            self.workTable.entered.connect(self.status_tip)
            self.workTable.doubleClicked.connect(self.reprint_work)
            self.search.textEdited.connect(self.search_)
            self.previousSetup.clicked.connect(self.previous_setup)
            self.newSetup.clicked.connect(self.new_setup)
            self.nextSetup.clicked.connect(self.next_setup)
            self.orderWork.clicked.connect(self.new_work_order)
        QtGui.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon(":/icons/parts.png"))

        self.layout = QtGui.QGridLayout(self)

        self.partNumber = QtGui.QLabel("Part Number", self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.partNumber.setFont(font)
        part_spacer = QtGui.QSpacerItem(478, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.infoTabs = QtGui.QTabWidget(self)

        self.basic_info_tab = QtGui.QWidget()
        self.basic_info_layout = QtGui.QVBoxLayout(self.basic_info_tab)
        self.description_label = QtGui.QLabel("Description", self.basic_info_tab)
        self.description = QtGui.QLineEdit(self.basic_info_tab)
        self.material_label = QtGui.QLabel("Material", self.basic_info_tab)
        self.material = QtGui.QLineEdit(self.basic_info_tab)
        self.machine_label = QtGui.QLabel("Machine", self.basic_info_tab)
        self.machine = QtGui.QLineEdit(self.basic_info_tab)
        self.routing_label = QtGui.QLabel("Routing", self.basic_info_tab)
        self.routing = QtGui.QLineEdit(self.basic_info_tab)
        self.destination_label = QtGui.QLabel("Destination", self.basic_info_tab)
        self.destination = QtGui.QLineEdit(self.basic_info_tab)
        self.on_order_label = QtGui.QLabel("On Order", self.basic_info_tab)
        self.onOrder = QtGui.QLineEdit(self.basic_info_tab)
        self.onOrder.setReadOnly(True)
        self.notes_label = QtGui.QLabel("Notes", self.basic_info_tab)
        self.notes = QtGui.QPlainTextEdit(self.basic_info_tab)
        self.partId = QtGui.QLabel(self.basic_info_tab)
        self.partId.setAlignment(QtCore.Qt.AlignRight)

        set_max([self.description_label, self.material_label, self.machine_label, self.routing_label,
                 self.destination_label, self.on_order_label, self.notes_label], 18)
        set_max([self.description, self.material, self.machine, self.routing, self.destination, self.onOrder], 24)

        self.basic_info_layout.addWidget(self.description_label)
        self.basic_info_layout.addWidget(self.description)
        self.basic_info_layout.addWidget(self.material_label)
        self.basic_info_layout.addWidget(self.material)
        self.basic_info_layout.addWidget(self.machine_label)
        self.basic_info_layout.addWidget(self.machine)
        self.basic_info_layout.addWidget(self.routing_label)
        self.basic_info_layout.addWidget(self.routing)
        self.basic_info_layout.addWidget(self.destination_label)
        self.basic_info_layout.addWidget(self.destination)
        self.basic_info_layout.addWidget(self.on_order_label)
        self.basic_info_layout.addWidget(self.onOrder)
        self.basic_info_layout.addWidget(self.notes_label)
        self.basic_info_layout.addWidget(self.notes)
        self.basic_info_layout.addStretch(1)
        self.basic_info_layout.addWidget(self.partId)

        self.machine_tab = QtGui.QWidget()

        self.machine_layout = QtGui.QVBoxLayout(self.machine_tab)
        self.machine_label_m = QtGui.QLabel("Machine", self.machine_tab)
        self.machine_m = QtGui.QLineEdit(self.machine_tab)
        self.machine_m.setReadOnly(True)
        self.routing_label_m = QtGui.QLabel("Routing", self.machine_tab)
        self.routing_m = QtGui.QLineEdit(self.machine_tab)
        self.routing_m.setReadOnly(True)
        self.material_label_m = QtGui.QLabel("Material", self.machine_tab)
        self.material_m = QtGui.QLineEdit(self.machine_tab)
        self.material_m.setReadOnly(True)
        self.blank_length_label = QtGui.QLabel("Blank Length", self.machine_tab)
        self.blankLength = QtGui.QLineEdit(self.machine_tab)
        self.program_label = QtGui.QLabel("Program", self.machine_tab)
        self.program = QtGui.QLineEdit(self.machine_tab)
        self.clamp_label = QtGui.QLabel("Clamp", self.machine_tab)
        self.clamp = QtGui.QLineEdit(self.machine_tab)

        self.machine_info_layout = QtGui.QGridLayout()
        self.bar_pull_label = QtGui.QLabel("Bar Pull", self.machine_tab)
        self.barPull = QtGui.QLineEdit(self.machine_tab)
        self.square_set_label = QtGui.QLabel("Square Set", self.machine_tab)
        self.squareSet = QtGui.QLineEdit(self.machine_tab)
        self.pos_stop_label = QtGui.QLabel("Positive Stop", self.machine_tab)
        self.posStop = QtGui.QLineEdit(self.machine_tab)

        self.machine_info_layout.addWidget(self.bar_pull_label, 0, 0, 1, 1)
        self.machine_info_layout.addWidget(self.barPull, 1, 0, 1, 1)
        self.machine_info_layout.addWidget(self.square_set_label, 0, 1, 1, 1)
        self.machine_info_layout.addWidget(self.squareSet, 1, 1, 1, 1)
        self.machine_info_layout.addWidget(self.pos_stop_label, 0, 2, 1, 1)
        self.machine_info_layout.addWidget(self.posStop, 1, 2, 1, 1)

        self.time_layout = QtGui.QGridLayout()
        self.cycle_label = QtGui.QLabel("Cycle", self.machine_tab)
        self.cycleTime = QtGui.QLineEdit(self.machine_tab)
        self.load_label = QtGui.QLabel("(Un)Load", self.machine_tab)
        self.loadTime = QtGui.QLineEdit(self.machine_tab)
        self.setup_label = QtGui.QLabel("Setup", self.machine_tab)
        self.setupTime = QtGui.QLineEdit(self.machine_tab)

        self.time_layout.addWidget(self.cycle_label, 0, 0, 1, 1)
        self.time_layout.addWidget(self.cycleTime, 1, 0, 1, 1)
        self.time_layout.addWidget(self.load_label, 0, 1, 1, 1)
        self.time_layout.addWidget(self.loadTime, 1, 1, 1, 1)
        self.time_layout.addWidget(self.setup_label, 0, 2, 1, 1)
        self.time_layout.addWidget(self.setupTime, 1, 2, 1, 1)

        set_max([self.machine_label_m, self.routing_label_m, self.material_label_m, self.blank_length_label,
                self.program_label, self.clamp_label, self.bar_pull_label, self.square_set_label, self.pos_stop_label,
                self.cycle_label, self.load_label, self.setup_label], 18)
        set_max([self.machine_m, self.routing_m, self.material_m, self.blankLength, self.program, self.clamp,
                 self.barPull, self.squareSet, self.posStop, self.cycleTime, self.loadTime, self.setupTime], 24)

        self.machine_layout.addWidget(self.machine_label_m)
        self.machine_layout.addWidget(self.machine_m)
        self.machine_layout.addWidget(self.routing_label_m)
        self.machine_layout.addWidget(self.routing_m)
        self.machine_layout.addWidget(self.material_label_m)
        self.machine_layout.addWidget(self.material_m)
        self.machine_layout.addWidget(self.blank_length_label)
        self.machine_layout.addWidget(self.blankLength)
        self.machine_layout.addWidget(self.program_label)
        self.machine_layout.addWidget(self.program)
        self.machine_layout.addWidget(self.clamp_label)
        self.machine_layout.addWidget(self.clamp)
        self.machine_layout.addLayout(self.machine_info_layout)
        self.machine_layout.addLayout(self.time_layout)
        self.machine_layout.addStretch(1)

        self.toolingTab = QtGui.QWidget()

        self.tooling_layout = QtGui.QGridLayout(self.toolingTab)
        self.toolingTable = QtGui.QTableView(self.toolingTab)
        tooling_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.addTooling = QtGui.QToolButton(self.toolingTab)
        self.addTooling.setText("+")

        self.tooling_layout.addWidget(self.toolingTable, 0, 0, 1, 2)
        self.tooling_layout.addItem(tooling_spacer, 1, 0, 1, 1)
        self.tooling_layout.addWidget(self.addTooling, 1, 1, 1, 1)

        self.infoTabs.addTab(self.basic_info_tab, "Info")
        self.infoTabs.addTab(self.machine_tab, "Machining")
        self.infoTabs.addTab(self.toolingTab, "Tooling")

        self.formTabs = QtGui.QTabWidget(self)

        self.printHolder = QtGui.QLabel(self)
        self.printHolder.setStyleSheet("background-color: rgb(240, 240, 240);")

        self.setupTab = QtGui.QWidget()
        self.setup_layout = QtGui.QGridLayout(self.setupTab)
        self.setupPic = QtGui.QLabel(self.setupTab)
        self.setupPic.setStyleSheet("background-color: rgb(240, 240, 240);")
        setup_spacer = QtGui.QSpacerItem(300, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.previousSetup = QtGui.QToolButton(self.setupTab)
        self.previousSetup.setMaximumSize(QtCore.QSize(24, 24))
        self.previousSetup.setArrowType(QtCore.Qt.LeftArrow)
        self.nextSetup = QtGui.QToolButton(self.setupTab)
        self.nextSetup.setMaximumSize(QtCore.QSize(24, 24))
        self.nextSetup.setArrowType(QtCore.Qt.RightArrow)
        self.setupIndex = QtGui.QLabel(self.setupTab)
        self.setupIndex.setMaximumSize(QtCore.QSize(100, 24))
        self.newSetup = QtGui.QToolButton(self.setupTab)
        self.newSetup.setMaximumSize(QtCore.QSize(24, 24))

        self.setup_layout.addWidget(self.setupPic, 0, 0, 1, 5)
        self.setup_layout.addItem(setup_spacer, 1, 0, 1, 1)
        self.setup_layout.addWidget(self.newSetup, 1, 1, 1, 1)
        self.setup_layout.addWidget(self.previousSetup, 1, 2, 1, 1)
        self.setup_layout.addWidget(self.nextSetup, 1, 3, 1, 1)
        self.setup_layout.addWidget(self.setupIndex, 1, 4, 1, 1)

        self.orderTable = QtGui.QTableView(self)

        self.workTable = QtGui.QTableView(self)
        self.workTable.setMouseTracking(True)

        self.updatesTab = QtGui.QWidget()
        self.update_layout = QtGui.QGridLayout(self.updatesTab)
        self.updateTable = QtGui.QTableView(self.updatesTab)
        update_spacer = QtGui.QSpacerItem(300, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.newUpdate = QtGui.QPushButton(self.updatesTab)

        self.update_layout.addWidget(self.updateTable, 0, 0, 1, 2)
        self.update_layout.addItem(update_spacer, 1, 0, 1, 1)
        self.update_layout.addWidget(self.newUpdate, 1, 1, 1, 1)

        self.formTabs.addTab(self.printHolder, "Print")
        self.formTabs.addTab(self.setupTab, "Setup")
        self.formTabs.addTab(self.orderTable, "Orders")
        self.formTabs.addTab(self.workTable, "Work Orders")
        self.formTabs.addTab(self.updatesTab, "Updates")

        self.bottom_layout = QtGui.QHBoxLayout(self)
        self.save = QtGui.QPushButton("Save", self)
        self.orderWork = QtGui.QPushButton("Order Work", self)
        self.search = QtGui.QLineEdit(self)
        self.search.setMinimumSize(QtCore.QSize(200, 24))
        self.search.setMaximumSize(QtCore.QSize(200, 24))
        self.search.setPlaceholderText("Search...")
        self.previous = QtGui.QToolButton(self)
        self.previous.setArrowType(QtCore.Qt.DownArrow)
        self.next = QtGui.QToolButton(self)
        self.next.setArrowType(QtCore.Qt.UpArrow)
        self.index = QtGui.QLabel(self)

        self.bottom_layout.addWidget(self.save)
        self.bottom_layout.addWidget(self.orderWork)
        self.bottom_layout.addStretch(1)
        self.bottom_layout.addWidget(self.search)
        self.bottom_layout.addWidget(self.previous)
        self.bottom_layout.addWidget(self.next)
        self.bottom_layout.addWidget(self.index)

        self.layout.addWidget(self.partNumber, 0, 0, 1, 1)
        self.layout.addItem(part_spacer, 0, 1, 1, 1)
        self.layout.addWidget(self.infoTabs, 1, 0, 1, 1)
        self.layout.addWidget(self.formTabs, 1, 1, 1, 3)
        self.layout.addLayout(self.bottom_layout, 0, 2, 1, 2)

        self.read_settings()
        connections()
        self.load_data()
        self.setup_comp()
        
    def load_data(self, part=None):
        """
        Get records from the view 'parts'.
        If 'part' isn't 'None', go find the right record.
        If 'part' is 'None', move to the first record.
        Then set the data to the form.
        """
        self.data_qry = QtSql.QSqlQuery()
        if self.data_qry.exec_("select * from parts"):
            #If part has data, try to find a matching part id. If one is found 
            #load that record, otherwise load the first record.
            if part:
                found = False
                while self.data_qry.next():
                    if self.data_qry.value(17).toString() == part:
                        found = True
                        break
                if not found:
                    QtGui.QMessageBox.critical(self, "Not Found", "The part could not be found")
                    self.data_qry.first()
            else:
                self.data_qry.first()
            self.set_data()
        else:
            db_err(self.data_qry)
        
    def set_data(self):
        """
        This function should be called _after_ a record is set.
        Takes the the data from mysql and loads it into the GUI
        so the user can view and modify it.
        """
        rec = self.data_qry.record()
        self.partNumber.setText(rec.value(0).toString())
        self.setWindowTitle(rec.value(0).toString())
        self.description.setText(rec.value(1).toString())
        self.material.setText(rec.value(2).toString())
        self.material_m.setText(rec.value(2).toString())
        self.machine.setText(rec.value(3).toString())
        self.machine_m.setText(rec.value(3).toString())
        self.routing.setText(rec.value(4).toString())
        self.routing_m.setText(rec.value(4).toString())
        self.destination.setText(rec.value(5).toString())
        self.onOrder.setText(rec.value(6).toString())
        self.notes.setPlainText(rec.value(7).toString())
        self.program.setText(rec.value(8).toString())
        self.clamp.setText(rec.value(9).toString())
        self.barPull.setText(rec.value(10).toString())
        self.squareSet.setText(rec.value(11).toString())
        self.posStop.setText(rec.value(12).toString())
        self.cycleTime.setText(rec.value(13).toString())
        self.loadTime.setText(rec.value(14).toString())
        self.setupTime.setText(rec.value(15).toString())
        self.blankLength.setText(rec.value(16).toString())
        self.partId.setText(rec.value(17).toString())
        self.index.setText(rec.value(18).toString())
        self.load_print()
        self.load_tooling()
        self.load_setup()
        self.load_orders()
        self.load_work()
        self.load_updates()
        
    def load_tooling(self):
        """
        Looks to see if there is tooling data for the current record.
        If there is it is loaded onto the parts table.
        """
        tooling_qry = QtSql.QSqlQuery()
        tooling_data = ("Select toolId, operation, description, notes from toolingInfo join toolingSetup on "
                        "toolingInfo.toolId = toolingSetup.tooling where toolingSetup.setup = {0}"
                        ).format(self.index.text())
        if tooling_qry.exec_(tooling_data):
            tooling_mod = QtSql.QSqlQueryModel()
            tooling_mod.setQuery(tooling_qry)
            self.toolingTable.setModel(tooling_mod)
            self.toolingTable.resizeColumnsToContents()
        else:
            db_err(tooling_qry)
            self.toolingTable.clear()
        
    def load_print(self, event=None):
        """
        Try to load a print for the current part.
        See 'readSettings' for 'self.prints'.
        """
        print_file = '{0}/{1}.jpg'.format(self.prints, self.partNumber.text())
        print_pix = QtGui.QPixmap(print_file)
        if print_pix.isNull():
            self.printHolder.clear()
        else:
            print_pix = print_pix.scaled(self.printHolder.size(), 1)
            self.printHolder.setPixmap(print_pix)
        
    def load_setup(self):
        """
        Check the database to see if the current part
        has any setup photos associated with it.
        If there is at least one, setSetup.
        """
        self.setup_qry = QtSql.QSqlQuery()
        if self.setup_qry.exec_("Select location from setupPhotos where part=%s order by id" % self.partId.text()):
            if self.setup_qry.first():
                self.set_setup()
            else:
                self.setupPic.clear()
                self.setupIndex.setText('0 of 0')
        else:
            db_err(self.setup_qry)
        
    def set_setup(self, event=None):
        """
        Loads a setup photo for the current part.
        setupQry should be set on a valid index before this is called.
        See 'readSettings' for self.setupBase.
        """
        print_file = '{0}{1}'.format(self.setup_base, self.setup_qry.value(0).toString())
        setup_pix = QtGui.QPixmap(print_file)
        if setup_pix.isNull():
            self.setupPic.clear()
        else:
            self.setupPic.setPixmap(setup_pix.scaled(self.setupPic.size(), 1))
            self.setupIndex.setText('{0} of {1}'.format(self.setup_qry.at()+1, self.setup_qry.size()))
        
    def next_setup(self):
        if self.setup_qry.next():
            self.set_setup()
        elif self.setup_qry.first():
            self.set_setup()
        else:
            err = "There was an error finding the next record."
            QtGui.QMessageBox.critical(self, "Database Error", err)
        
    def previous_setup(self):
        if self.setup_qry.previous():
            self.set_setup()
        elif self.setup_qry.last():
            self.set_setup()
        else:
            err = "There was an error finding the previous record."
            QtGui.QMessageBox.critical(self, "Database Error", err)
    
    def new_setup(self):
        rec = self.index.text()
        part = self.partId.text()
        insert_qry = QtSql.QSqlQuery()
        if rec != '0':
            files = QtGui.QFileDialog.getOpenFileNames(None, "Add Photos", self.setup_base,'Images (*.jpg)', 'Images')
            for setup_file in files:
                setup_file = setup_file.replace(self.setup_base, '')
                setup_file = setup_file.replace('\\', '\\\\')
                qry = "Insert into setupPhotos (part, location) VALUES({0}, '{1}')".format(part, setup_file)
                if not insert_qry.exec_(qry):
                    db_err(insert_qry)
            self.load_data(part)
        
    def load_orders(self):
        """
        Get all the order records for the current part number.
        """
        orders_qry = QtSql.QSqlQuery()
        part = self.partNumber.text()
        orders_data = ("select `Part Num`as 'Part #', `Qty`, `Hot`, partOrder_qry.`Order_num` as 'Order #', `Name` as "
                       "'Ordered By', date_format(ODate, '%Y-%m-%d') as 'Date', `Tracking Num` as 'Tracking' from "
                       "inventorysystem.partOrder_qry join (inventorysystem.Orders_tbl join inventorysystem.Users_tbl "
                       "on Orders_tbl.User_ID = Users_tbl.User_ID) on partOrder_qry.Order_num = Orders_tbl.Order_num "
                       "where `Part Num` = '{0}' order by partOrder_qry.`Order_num` Desc").format(part)
        if orders_qry.exec_(orders_data):
            orders_mod = QtSql.QSqlQueryModel()
            orders_mod.setQuery(orders_qry)
            self.orderTable.setModel(orders_mod)
        else:
            db_err(orders_qry)
        
    def load_work(self):
        """
        Get all the work order records for the current part number.
        """
        work_qry = QtSql.QSqlQuery()
        work_data = ("Select Work_Details_tbl.Tracking_num as 'Tracking', Work_Details_tbl.Qty, Status_Description as "
                     "'Status', Date_Format(SDate, '%Y-%m-%d') as 'Date', Job_num as 'Job', Dest_Desc as 'Destination' "
                     "from inventorysystem.Work_Orders_tbl join((inventorysystem.Work_Details_tbl join "
                     "inventorysystem.Status_qry on Work_Details_tbl.Tracking_num = Status_qry.Tracking_num) join "
                     "inventorysystem.Destination_tbl on Work_Details_tbl.Dest_ID = Destination_tbl.Dest_ID) on "
                     "Work_Orders_tbl.Job_ID = Work_Details_tbl.Job_ID where Part_ID = {0} Order by JDate DESC"
                     ).format(self.partId.text())
        if work_qry.exec_(work_data):
            work_mod = QtSql.QSqlQueryModel()
            work_mod.setQuery(work_data)
            self.workTable.setModel(work_mod)
        else:
            db_err(work_qry)
        
    def reprint_work(self, index):
        """
        Called from the work order table.
        This generates paper work for the clicked record.
        Use this to reprint lost paper work or paper work for laser parts
        that need machining done also.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        mod = index.model()
        row = index.row()
        self.tracking = mod.data(mod.index(row, 0)).toString()
        print_ = QtGui.QPrintPreviewDialog()
        print_.paintRequested.connect(self.print_preview)
        print_.exec_()
        QtGui.QApplication.restoreOverrideCursor()
        
    def print_preview_(self, printer):
        """
        Part of reprint_work.
        """
        printer.setOrientation(1)
        printer.setPaperSize(printer.PageSize(2))
        printer.setPageSize(printer.PageSize(2))
        printer.setPageMargins(.25, .25, .25, .25, 2)
        printer.newPage()
        self.print_work = PrintWork(self.tracking)
        self.print_work.setGeometry(printer.pageRect())
        self.print_work.render(printer)
        
    def status_tip(self, index):
        """
        Load the work order status history into a tool tip.
        """
        mod = index.model()
        row = index.row()
        tnum = mod.data(mod.index(row, 0)).toString()
        self.status_qry = QtSql.QSqlQuery()
        status_data = ("Select Status_Description, Init, date_format(SDate, '%Y-%m-%d'), Finished, StatQty from "
                       "inventorysystem.Status_tbl join inventorysystem.Users_tbl on Status_tbl.User_ID = "
                       "Users_tbl.User_ID Where Tracking_num = {0} Order by SDate DESC").format(tnum)
        if self.status_qry.exec_(status_data):
            status_list = ""
            if self.status_qry.first():
                status_list += ("{0}, {1}, {2}, {3}, {4}".format(self.status_qry.value(0).toString(),
                                                                 self.status_qry.value(1).toString(),
                                                                 self.status_qry.value(2).toString(),
                                                                 self.status_qry.value(3).toString(),
                                                                 self.status_qry.value(4).toString()))
            while self.status_qry.next():
                status_list += ("\n{0}, {1}, {2}, {3}, {4}".format(self.status_qry.value(0).toString(),
                                                                   self.status_qry.value(1).toString(),
                                                                   self.status_qry.value(2).toString(),
                                                                   self.status_qry.value(3).toString(),
                                                                   self.status_qry.value(4).toString()))
            self.workTable.setToolTip(status_list)

    def load_updates(self):
        """
        Get all the update records for the current part number.
        """
        update_qry = QtSql.QSqlQuery()
        update_data = ("Select Part_num as 'Part #', date_format(UDate, '%Y-%m-%d') as 'Date', Update_Desc as 'Update',"
                       " New from inventorysystem.Updates_tbl join inventorysystem.Parts_tbl on Updates_tbl.Part_ID = "
                       "Parts_tbl.Part_ID WHERE Parts_tbl.Part_ID = {0}").format(self.partId.text())
        if update_qry.exec_(update_data):
            update_mod = QtSql.QSqlQueryModel()
            update_mod.setQuery(update_qry)
            self.updateTable.setModel(update_mod)
        else:
            db_err(update_qry)
        
    def expand_print(self, event):
        """
        Expand the print to fullscreen. Closes on click.
        """
        part = self.partNumber.text()
        exprint = PrintView("{0}/{1}.jpg".format(self.prints, part), self)
        exprint.exec_()
        
    def next_(self):
        """
        Try to move to the next record. If there isn't a next record loop to
        the first record. Reset the data on the GUI.
        """
        if self.data_qry.next():
            self.set_data()
        elif self.data_qry.first():
            self.set_data()
        else:
            err = "There was an error finding the next record."
            QtGui.QMessageBox.critical(self, "Database Error", err)
        
    def previous_(self):
        """
        Try to move to the previous record. If there isn't a previous
        record loop to the first record. Reset the data on the GUI.
        """
        if self.data_qry.previous():
            self.set_data()
        elif self.data_qry.last():
            self.set_data()
        else:
            err = "There was an error finding the previous record."
            QtGui.QMessageBox.critical(self, "Database Error", err)
        
    def wheel_navi(self, event):
        """
        Enables the use of the scroll wheel to navigate records.
        Delta is positive in one direction and negative in the other direction.
        """
        directory = event.delta()
        if directory > 0: 
            self.next_()
        else:
            self.previous_()
        
    def search_(self, text):
        """
        Very simple search function.
        It moves to the first record then iterates though all the records until
        it finds on the matches. If it finds a record it loads the data and 
        breaks the loop. Otherwise the loop will end and it will load the 
        last record of the query.
        """
        self.data_qry.first()
        while self.data_qry.next():
            if text in self.data_qry.value(0).toString():
                break
        self.set_data()
        
    def setup_comp(self):
        """
        Load the data for the completer on material, machine, destination
        and process. This is important so that correct values are entered when
        editing parts.
        """
        comp_qry = QtSql.QSqlQuery()
        if comp_qry.exec_("Select material from material"):
            mat_list = []
            while comp_qry.next():
                mat_list.append(comp_qry.value(0).toString())
            mat_comp = QtGui.QCompleter(mat_list, self.material)
            mat_comp.setCaseSensitivity(0)
            self.material.setCompleter(mat_comp)
        else:
            db_err(comp_qry)
        if comp_qry.exec_("Select name from machines"):
            machine_list = []
            while comp_qry.next():
                machine_list.append(comp_qry.value(0).toString())
            machine_comp = QtGui.QCompleter(machine_list, self.machine)
            machine_comp.setCaseSensitivity(0)
            self.machine.setCompleter(machine_comp)
        else:
            db_err(comp_qry)
        if comp_qry.exec_("Select Process from setupInfo group by Process"):
            routing_list = []
            while comp_qry.next():
                routing_list.append(comp_qry.value(0).toString())
            routing_comp = QtGui.QCompleter(routing_list, self.routing)
            routing_comp.setCaseSensitivity(0)
            self.routing.setCompleter(routing_comp)
        else:
            db_err(comp_qry)
        if comp_qry.exec_("Select Dest_Desc from inventorysystem.Destination_tbl"):
            destination_list = []
            while comp_qry.next():
                destination_list.append(comp_qry.value(0).toString())
            destination_comp = QtGui.QCompleter(destination_list, self.destination)
            destination_comp.setCaseSensitivity(0)
            self.destination.setCompleter(destination_comp)
        else:
            db_err(comp_qry)
        
    def add_tooling(self):
        """
        Adds new tooling to the current part.
        """
        if self.index.text() != '0':
            add_tooling = AddTooling(self.index.text(), self)
            add_tooling.exec_()
            self.load_tooling()
        
    def save_(self):
        """
        This function is huge...
        This saves all the data associated with the current part.
        It starts by saving the basic info to Doyle's database. This is the
        slowest part because of the connection problems.
        After that, if all the info is filled out, it saves the machining
        specific data to Riverview's database. To do this it has to look up the
        machine and material to get the right id numbers. If the user enters an
        invalid machine, 'N/A' is substituted. For material, the new material
        is added to the system and the new id is retrieved and used.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        # Open a connection to Doyle's database.
        self.dbw, ok = write_connection(self)
        save_qry = QtSql.QSqlQuery()
        while ok:
            descp = prepare_string(self.description.text())
            dest = prepare_string(self.destination.text())
            notes = prepare_string(self.notes.toPlainText())
            # User must at least have a description and destination to save.
            if descp != "" and dest != "":
                dest_qry = "Select Dest_ID from inventorysystem.Destination_tbl where Dest_Desc = '{0}'".format(dest)
                if save_qry.exec_(dest_qry): # Get the destination id.
                    if save_qry.first():
                        dest = save_qry.value(0).toString()
                    else:
                        dest = '7'
                else:
                    db_err(save_qry)
                    dest = '7'
                qry = ("update inventorysystem.Parts_tbl set Part_Desc='{0}', Part_Notes='{1}',destination={2} where "
                       "Part_ID = {3}").format(descp, notes, dest, self.partId.text())
                write_qry = QtSql.QSqlQuery(self.dbw)
                if not write_qry.exec_(qry):
                    db_err(write_qry)
            break
        del self.dbw
        mach = self.machine.text()
        cycle = self.cycleTime.text()
        load = self.loadTime.text()
        setup = self.setupTime.text()
        mat = self.material.text()
        clamp = self.clamp.text()
        blank_length = self.blankLength.text()
        bar = self.barPull.text()
        square = self.squareSet.text()
        pos_stop = self.posStop.text()
        proc = self.routing.text()
        prog_file = self.program.text()
        if mach != "" and mat != "" and proc != "":
            mach_qry = "Select id from machines where name = '{0}'".format(mach)
            if save_qry.exec_(mach_qry):
                if save_qry.first():
                    mach = save_qry.value(0).toString()
                else:
                    mach = "14"
            else:
                db_err(save_qry)
                mach = "14"
            mat_qry = "Select id from material where material = '{0}'".format(mat)
            if save_qry.exec_(mat_qry):
                if save_qry.first():
                    mat = save_qry.value(0).toString()
                else:
                    if save_qry.exec_("insert into material set material='{0}'".format(mat)):
                        mat = save_qry.lastInsertId().toString()
                    else:
                        db_err(save_qry)
                        mat = "17"
            else:
                db_err(save_qry)
                mat = "17"
            qry2 = ("machine={0}, cycleTime=time_to_Sec('{1}'), loadTime=time_to_Sec('{2}'), "
                    "setupTime=time_to_Sec('{3}'), material={4}, clampPSI={5}, blankLength={6}, barPull={7}, "
                    "squareSet={8}, posStop={9}, Process='{10}', fileName='{11}'"
                    ).format(mach, cycle, load, setup, mat, clamp, blank_length, bar, square, pos_stop, proc, prog_file)
            if self.index.text() == '0':
                part_id = self.partId.text()
                qry2 = ("Insert into setupInfo set {0}, partId={1}".format(qry2, part_id))
            else:
                qry2 = ("Update setupInfo set {0} where id={1}".format(qry2, self.index.text()))
            local_qry = QtSql.QSqlQuery()
            if not local_qry.exec_(qry2):
                db_err(local_qry)
        self.load_data(self.partId.text())
        QtGui.QApplication.restoreOverrideCursor()

    def new_work_order(self):
        self.part = self.partId.text()
        self.part_num = self.partNumber.text()
        qty = int(self.onOrder.text())
        text = "How many of {0} for this work order?".format(self.part_num)
        self.qty, ok = QtGui.QInputDialog.getInt(self, "Order Quantity", text, qty)
        if ok:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.tracking, ok = save_work_order(self.part, self.qty)
            if ok:
                print_ = QtGui.QPrintPreviewDialog()
                print_.paintRequested.connect(self.print_preview)
                print_.exec_()
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

####Settings Block
    def read_settings(self):
        settings = QtCore.QSettings("Riverview", "Machining")
        settings.beginGroup("Main")
        self.prints = settings.value("prints", None).toString()
        self.setup_base = settings.value("setup", None).toString()
        settings.endGroup()
        if self.prints == "":
            self.prints = QtGui.QFileDialog.getExistingDirectory(self, "Prints Location")
            self.write_settings(self.prints, self.setup_base)
        if self.setup_base == "":
            self.setup_base = QtGui.QFileDialog.getExistingDirectory(self, "Setup Pictures Location")
            self.write_settings(self.prints, self.setup_base)
        
    def write_settings(self, prints, setup):
        settings = QtCore.QSettings("Riverview", "Machining")
        settings.beginGroup("Main")
        settings.setValue("prints", prints)
        settings.setValue("setup", setup)
        settings.endGroup()
####


class PrintView(QtGui.QDialog):
    def __init__(self, print_, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.printHolder = QtGui.QLabel(self)
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.printHolder)
        self.printHolder.mousePressEvent = self.done_
        
        self.print_ = print_
        self.printHolder.resizeEvent = self.load_print
        self.showMaximized()
        
    def done_(self, event):
        self.done(1)
        
    def load_print(self, event):
        print_image = QtGui.QPixmap(self.print_)
        if not print_image.isNull():
            self.printHolder.setPixmap(print_image.scaled(self.printHolder.size(), 1, 1))
        else:
            self.printHolder.clear()


class AddTooling(QtGui.QDialog):
    def __init__(self, setup, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(350, 200)
        self.setWindowTitle("Add Tool")
        self.setWindowIcon(QtGui.QIcon(":/icons/parts.png"))

        self.tool_label = QtGui.QLabel("Tool Number", self)
        self.operation_label = QtGui.QLabel("Operation", self)
        self.description_label = QtGui.QLabel("Description", self)
        self.notes_label = QtGui.QLabel("Notes", self)

        self.notes = QtGui.QLineEdit(self)
        self.tool_num = QtGui.QLineEdit(self)
        self.op = QtGui.QLineEdit(self)
        self.desc = QtGui.QLineEdit(self)
        self.cancel = QtGui.QPushButton("Cancel", self)
        self.add = QtGui.QPushButton("Add", self)

        self.layout = QtGui.QGridLayout(self)
        self.layout.addWidget(self.tool_label, 0, 0, 1, 1)
        self.layout.addWidget(self.operation_label, 1, 0, 1, 1)
        self.layout.addWidget(self.description_label, 2, 0, 1, 1)
        self.layout.addWidget(self.notes_label, 3, 0, 1, 1)
        self.layout.addWidget(self.notes, 3, 1, 1, 1)
        self.layout.addWidget(self.tool_num, 0, 1, 1, 1)
        self.layout.addWidget(self.op, 1, 1, 1, 1)
        self.layout.addWidget(self.desc, 2, 1, 1, 1)
        self.layout.addWidget(self.cancel, 4, 0, 1, 1)
        self.layout.addWidget(self.add, 4, 1, 1, 1)

        self.setup = setup
        self.cancel.clicked.connect(self.cancel_)
        self.add.clicked.connect(self.add_)
        self.new_tool = True
        tools_qry = QtSql.QSqlQuery()
        if tools_qry.exec_("select toolId from toolingInfo"):
            tools = []
            while tools_qry.next():
                tools.append(tools_qry.value(0).toString())
            tool_comp = QtGui.QCompleter(tools)
            self.tool_num.setCompleter(tool_comp)
            self.tool_num.textChanged.connect(self.check_tool)
            self.tool_num.editingFinished.connect(self.load_tool_info)
        else:
            db_err(tools_qry)
        
    def check_tool(self, text):
        if self.tool_num.completer().completionCount() > 0:
            self.new_tool = False
        else:
            self.new_tool = True
        
    def load_tool_info(self):
        if not self.new_tool:
            tools_qry = QtSql.QSqlQuery()
            tool_data = ("Select toolId, operation, description, notes from "
                         "toolingInfo where toolId = {0}").format(self.tool_num.text())
            if tools_qry.exec_(tool_data):
                if tools_qry.first():
                    tool = tools_qry.value(0).toString()
                    op = tools_qry.value(1).toString()
                    desc = tools_qry.value(2).toString()
                    notes = tools_qry.value(3).toString()
                    self.tool_num.setText(tool)
                    self.op.setText(op)
                    self.desc.setText(desc)
                    self.notes.setText(notes)
                else:
                    self.op.clear()
                    self.desc.clear()
                    self.notes.clear()
            else:
                db_err(tools_qry)
                self.op.clear()
                self.desc.clear()
                self.notes.clear()
        
    def add_(self):
        tools_qry = QtSql.QSqlQuery()
        tool = self.tool_num.text()
        op = self.op.text()
        desc = self.desc.text()
        notes = self.notes.text()
        if tool != '' and op != '':
            if tools_qry.exec_("Select toolId from toolingInfo where toolId = '{0}'".format(tool)):
                print tools_qry.size()
                if tools_qry.size() == 0:
                    tools_insert = ("Insert into toolingInfo (toolId, operation, description, notes) "
                                    "VALUES('{0}', '{1}', '{2}', '{3}')").format(tool, op, desc, notes)
                    if not tools_qry.exec_(tools_insert):
                        db_err(tools_qry)
                        self.done(0)
                tools_insert = "insert into toolingSetup (setup, tooling) VALUES({0}, {1})".format(self.setup, tool)
                print tools_insert
                if tools_qry.exec_(tools_insert):
                    self.done(1)
                else:
                    db_err(tools_qry)
                    self.done(0)
            else:
                db_err(tools_qry)
                self.done(0)
        else:
            self.op.setFocus()
        
    def cancel_(self):
        self.done(0)
