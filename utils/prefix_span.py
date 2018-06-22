import numpy as np
from prefixspan import PrefixSpan

class PrefixSpanManager:

    def __init__(self, sax_engine, export = True):
        self.se_instance = sax_engine
        self.data = sax_engine.sax_data
        self.process_data = []
        self.ps = None
        if export:
            self.export_format()

    def run(self):
        self.ps = PrefixSpan(self.process_data)

    def export_format(self):
        tmp = []
        for elmt in self.data:
            tmp.append(elmt.ravel())
        self.process_data = tmp
