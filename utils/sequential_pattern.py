import pandas as pd
import numpy as np

from tslearn.piecewise import SymbolicAggregateApproximation
from prefixspan import PrefixSpan

class SequentialPattern:
    """
    Etude des motifs dans un dataset de series temporelles
    """
    def __init__(self):
        self.raw_data = None
        self.transformed_data = None
        self.sax_data_inv = None
        self.sax_data = None
        self.sax = None
        self.ps = None
        self.nb_symbol = 8
        self.nb_segment = 21

    def set_nb_symbol(self, nb):
        if nb > 0:
            self.nb_symbol = nb
        else:
            print("Valeur incorrecte")

    def set_nb_segment(self, nb):
        if nb > 0:
            self.nb_segment = nb
        else:
            print("Valeur incorrecte")

    def fit(self, data):
        self.raw_data = data

    def export_format(self):
        data = []
        for elmt in self.raw_data:
            data.append(elmt.ravel())
        self.transformed_data = data

    def fit_export(self, data):
        self.fit(data)
        self.export_format()

    def sax_engine(self):
        self.sax = SymbolicAggregateApproximation(n_segments = self.nb_segment, alphabet_size_avg = self.nb_symbol)
        sax_dataset = self.sax.fit_transform(self.raw_data)
        sax_dataset_inv = self.sax.inverse_transform(self.sax.fit_transform(self.raw_data))

    def prefixspan(self):
        self.ps = PrefixSpan(self.transformed_data)
