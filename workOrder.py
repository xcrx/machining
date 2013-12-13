from PyQt4 import QtGui, QtSql
from dbConnection import write_connection, db_err


def save_work_order(part, qty):
    dest_qry = QtSql.QSqlQuery()
    dest_data = "Select destination from inventorysystem.Parts_tbl where Part_ID = {0}".format(part)
    if dest_qry.exec_(dest_data):
        if dest_qry.first():
            dest = dest_qry.value(0).toString()
        else:
            QtGui.QMessageBox.critical(None, "Error", "The part could not be found")
    else:
        QtGui.QMessageBox.critical(None, "Database Error", dest_qry.lastError().text())
    qry = "Insert into Work_Details_tbl (Job_ID, Part_ID, Qty, Dest_ID) VALUES(5536,{},{},{})".format(part, qty, dest)
    dbw, ok = write_connection(None)
    if not ok:
        return
    dbw.transaction()
    wo_qry = QtSql.QSqlQuery(db=dbw)
    if wo_qry.exec_(qry):
        tracking = wo_qry.lastInsertId().toString()
        status, ok = QtGui.QInputDialog.getText(None, "Enter Status", "Status:", text="Saw")
        if not ok:
            dbw.rollback()
            return None, False
        qry = ("Insert into Status_tbl (Status_Description, User_ID, Tracking_num, StatQty) VALUES('{2}', 8, {0}, {1})"
               ).format(tracking, qty, status)
        if wo_qry.exec_(qry):
            del wo_qry
            dbw.commit()
            return tracking, True
        else:
            db_err(wo_qry)
            dbw.rollback()
            return None, False
    else:
        db_err(wo_qry)
        dbw.rollback()
        return None, False