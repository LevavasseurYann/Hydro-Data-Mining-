import numpy as np
from prefixspan import PrefixSpan
from utils.plot import Plot

class PrefixSpanManager:

    def __init__(self, sax_engine, export = True):
        self.se_instance = sax_engine
        self.data = sax_engine.sax_data
        self.process_data = []
        self.ps = None
        self.ploter = Plot(self)
        if export:
            self.export_format()

    def run(self):
        self.ps = PrefixSpan(self.process_data)

    def export_format(self):
        tmp = []
        for elmt in self.data:
            tmp.append(elmt.ravel())
        self.process_data = tmp

    def topk(self, n, c = True):
        return self.ps.topk(n, closed = c)

    def frequent(self, n):
        return self.ps.frequent(n)

    def plot(self, l):
        self.ploter.plot_prefixspan(l)
