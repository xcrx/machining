from PyQt4 import QtGui, QtSql, QtCore, uic


def default_connection():
    """
    Opens the 'read' database connection
    although I am calling this connection the 'read' connection,
    it is used to write to the machining database also. 
    
    This isn't the best way to do this but it will work as a temp solution.
    """
    if QtSql.QSqlDatabase.database().open():
        return True
    else:
        db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        host, database = read_settings('default')
        db.setHostName(host)
        db.setDatabaseName(database)
        db.setUserName('riverview')
        db.setPassword('riverview')
        db.setPort(3306)
        if db.open():
            return True
        else:
            db_err(db)


def write_connection():
    """
    Opens a connection to the main server.
    This is used to write updates and inserts for parts and
    work orders. It is slow to connect and use due to bandwidth.
    """
    if QtSql.QSqlDatabase.database('write').open():
        db = QtSql.QSqlDatabase.database('write')
        return db, True
    else:
        db = QtSql.QSqlDatabase.addDatabase("QMYSQL", "write")
        host, database = read_settings('write')
        db.setHostName(host)
        db.setDatabaseName(database)
        db.setUserName('riverview')
        db.setPassword('riverview')
        db.setPort(3306)
        if db.open():
            return db, True
        else:
            db_err(db)
            return None, False

    
def db_err(qry=None):
    if qry is not None:
        try:
            QtGui.QMessageBox.critical(None, 'Database Error', qry.lastError().text())
            return
        except:
            pass
    QtGui.QMessageBox.critical(None, 'Database Error', "An unknown database error occurred.")


def start_transaction(db='qt_sql_default_connection'):
    db = QtSql.QSqlDatabase.database(db)
    if db.transaction():
        return True
    else:
        print db.lastError().text()
        QtGui.QMessageBox.critical(None, "Transaction Error", "Could not start the transaction.")
        return False


def commit_transaction(db='qt_sql_default_connection'):
    db = QtSql.QSqlDatabase.database(db)
    if db.commit():
        return True
    else:
        QtGui.QMessageBox.critical(None, "Transaction Error", "Could not commit the transaction.")
        return False


def rollback_transaction(db='qt_sql_default_connection'):
    db = QtSql.QSqlDatabase.database(db)
    return db.rollback()


####Settings Block
def write_settings(host, database, group):
    settings = QtCore.QSettings("Riverview", "Machining")
    settings.beginGroup(group)
    settings.setValue('host', QtCore.QString(host))
    settings.setValue('database', QtCore.QString(database))
    settings.endGroup()


def read_settings(group):
    settings = QtCore.QSettings("Riverview", "Machining")
    settings.beginGroup(group)
    host = settings.value('host', None).toString()
    database = settings.value('database', None).toString()
    if host == '' or database == '':
        db_settings = DatabaseSettings()
        while host == '' or database == '':
            host, database = db_settings.get_data()
        if not host == 'Null' or database == 'Null':
            write_settings(host, database, group)
    return host, database


class DatabaseSettings(QtGui.QDialog):
    """
    Simple dialog for entering database settings.
    """
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi('ui/databaseSettings.ui', self)
        
    def get_data(self):
        self.exec_()
        host = self.hostname.text()
        database = self.database.text()
        if host != "":
            if database != "":
                return host, database
            else:
                self.database.setFocus()
                return host, 'Null'
        else:
            self.hostname.setFocus()
            return 'Null', 'Null'
    
    def reject(self):
        self.done(0)
