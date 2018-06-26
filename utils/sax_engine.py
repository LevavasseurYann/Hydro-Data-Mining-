import numpy as np
from tslearn.piecewise import SymbolicAggregateApproximation

class SaxEngine:
    """
    Etude des motifs dans un dataset de series temporelles
    """
    def __init__(self, nsy, nse):
        self.raw_data = []
        self.process_data = []
        self.sax_data_inv = []
        self.sax_data = []
        self.nb_symbol = nsy
        self.nb_segment = nse
        #self.sax = None

    def reset(self):
        self.raw_data = []
        self.process_data = []
        self.sax_data_inv = []
        self.sax_data = []

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

    def fit(self, data, export = True):
        self.raw_data = data
        if export:
            self.export_format()
        else:
            self.process_data = data

    def export_format(self):
        tmp = []
        for elmt in self.raw_data:
            tmp.append(np.expand_dims(elmt, axis=0))
        self.process_data = tmp

    def step_run(self, data):
        sax = SymbolicAggregateApproximation(n_segments = self.nb_segment, alphabet_size_avg = self.nb_symbol)
        sax_dataset = sax.fit_transform(data)
        sax_dataset_inv = sax.inverse_transform(sax_dataset)
        return sax_dataset, sax_dataset_inv

    def run(self):
        self.sax_data = []
        self.sax_data_inv = []
        for elmt in self.process_data:
            step = self.step_run(elmt)
            self.sax_data.append(step[0])
            self.sax_data_inv.append(step[1])

    def fit_run(self, data):
        self.fit(data)
        self.run()
