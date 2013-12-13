from PyQt4 import QtSql, QtGui
import sys
from dbConnection import db_err

part_to_id = "Select Part_ID from inventorysystem.Parts_tbl where Part_num = '{0}'"

get_qty = "Select Qty from inventorysystem.Work_Details_tbl where Tracking_num={0}"

new_status = ("Update Work_Details_tbl set Qty={3} where Tracking_Num = {1}; "
              "Insert into Status_tbl (Status_Description, Tracking_num, Finished, StatQty, User_ID) "
              "VALUES('{0}',{1},'{2}',{3}, 8)")

get_machine_id = "Select id from machines where name='{0}'"

get_machines = "Select name from machines"

update_schedule = "Update schedule set machine={0} where trackingId={1}"

active_orders = ("Select `Part #`, `Description`, `On Order`, `Short`, `In Process`, `Process`, `Material`, "
                 "`Est. Mat.`, `Est. Time`, `partId` from orders where `On Order` > 0")

setup_orders = "Select `Part #`, `Description`, `On Order` from orders where Machine is Null and `On Order` > 0"

material_orders = ("Select `Part #`, `Description`, `On Order`, `Material`, `Est. Mat.`, `Av. Mat.`, partId "
                   "from orders where (`Av. Mat.` - `Est. Mat.`) < 0 and `On Order` > 0")

in_process_orders = ("Select `Part #`, `Description`, `On Order`, `Short`, `In Process`, `Process`, `Material`, "
                     "`Est. Mat.`, `Est. Time`, `partId` from orders where `In Process` > 0")


def query(data, args=None, db='qt_sql_default_connection'):
    qry = QtSql.QSqlQuery(db)
    try:
        data = getattr(sys.modules[__name__], data)
    except AttributeError:
        QtGui.QMessageBox.critical(None, "Query Not Found", "A query matching %s was not found. Typo?" % data)
        return False
    if args:
        data = data.format(*args)
    if qry.exec_(data):
        return qry
    else:
        db_err(qry)
        return False