import numpy as np
from prefixspan import PrefixSpan
from utils.plot import Plot

class PrefixSpanManager:
    """
    Classe d'outil a l'utilisation de prefixspan

    Parameters:
        * sax_engine: SaxEngine
            Instance de preprocessing SAX
        * export: Boolean
            Si oui ou non les donnees sont deja exportees au bon format

    Variables:
        * se_instance: SaxEngine
            L'instance de class SAX
        * data: Array[]
            Les donnees au format SAX
    """
    def __init__(self, sax_engine, export = True):
        self.se_instance = sax_engine
        self.data = sax_engine.sax_data
        self.process_data = []
        self.ps = None
        self.ploter = Plot(self)
        if export:
            self.export_format()

    def run(self):
        """
        Creer l'instance PrefixSpan avec les donnees pretraites
        """
        self.ps = PrefixSpan(self.process_data)

    def export_format(self):
        """
        Modifie le format pour correspondre au besoin de l'instance de PrefixSpan
        """
        tmp = []
        for elmt in self.data:
            tmp.append(elmt.ravel())
        self.process_data = tmp

    def topk(self, n, c = True):
        """
        Affiche les motifs les plus frequents(plus grand support) et par defaut les fermes

        Parameters:
            * n: int
                Nombre de motifs a afficher
        Returns:
            Liste de motifs frequent
        """
        return self.ps.topk(n, closed = c)

    def frequent(self, n):
        """
        Retourne les frequent de support n

        Parameters:
            * n: int
                Support minimal
        Returns:
            Liste des motifs de support minimal n
        """
        return self.ps.frequent(n)

    def plot(self, l):
        self.ploter.plot_prefixspan(l)
