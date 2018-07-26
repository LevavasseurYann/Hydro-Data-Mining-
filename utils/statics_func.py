# STATICS METHODS
def openfile_dialog():
    """
    Boite de dialogue permetant de recuperer les fichers de sauvegarde de partitionnement Pickle

    Parameters
    ----------
    NA

    Returns
    -------
    fname: String
        Chemin vers le fichier selectionne
    """
    from PyQt5 import QtGui
    from PyQt5 import QtGui, QtWidgets
    app = QtWidgets.QApplication([dir])
    frame = QtWidgets.QFileDialog
    #fname, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Select a pkl file", '.', filter="*.pkl")
    fname = QtWidgets.QFileDialog.getOpenFileName(None, "Select pkl file", "", "Pickle file (*.pkl)")
    return fname

import numpy as np
import pylab

# Fonction de dedection de pics
def thresholding_algo(y, lag, threshold, influence):
    """
    Algorithm de detection de pics dans une TS

    Parameters
    ----------
    lag
    threshold
    influence

    Returns
    -------
    unnamed: {Dict}
        Informations sortie de l'algo, signals est une liste de meme len que la TS, representant les ppics via une variation boolean
    """
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))

COLORS = ["red", "green", "yellow", "blue", "orange", "purple", "cyan", "magenta", "pink", "gold", "chartreuse", "navy", "magenta", "peru", "royal blue",
    "red", "green", "yellow", "blue", "orange", "purple", "cyan", "magenta", "pink", "gold", "chartreuse", "navy", "magenta", "peru", "royal blue"]
