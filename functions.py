from PyQt4 import QtGui, QtCore
from query import query


def partnum_to_partid(partnum):
    """
    Takes a part number as input and returns the part id
    for it if it has one. Returns None if if doesn't.
    """
    qry = query("part_to_id", [partnum])
    if qry:
        if qry.first():
            return qry.value(0).toString()
        else:
            return None
    else:
        return None


def restore_cursor():
    while QtGui.QApplication.overrideCursor():
        QtGui.QApplication.restoreOverrideCursor()

def set_statusbar(self, text, timeout=0):
    sec = 1000
    self.statusBar().showMessage(text, timeout*sec)
    self.repaint()


def write_settings(name, value):
    settings = QtCore.QSettings("Doyle Mfg", "Post_Laser_Schedule")
    settings.setDefaultFormat(1)
    settings.beginGroup('main')
    settings.setValue(name, value)
    settings.endGroup()


def read_settings(name):
    settings = QtCore.QSettings("Doyle Mfg", "Post_Laser_Schedule")
    settings.setDefaultFormat(1)
    settings.beginGroup('main')
    value = settings.value(name, None)
    return value