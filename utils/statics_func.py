# STATICS METHODS
def openfile_dialog():
    from PyQt5 import QtGui
    from PyQt5 import QtGui, QtWidgets
    app = QtWidgets.QApplication([dir])
    frame = QtWidgets.QFileDialog
    #fname, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Select a pkl file", '.', filter="*.pkl")
    fname = QtWidgets.QFileDialog.getOpenFileName(None, "Select pkl file", "", "Pickle file (*.pkl)")
    return fname
