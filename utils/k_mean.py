from tslearn.clustering import TimeSeriesKMeans
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, TimeSeriesResampler
from tslearn.utils import to_time_series
from tslearn.utils import to_time_series_dataset
from collections import Counter
import numpy as np

from utils.cluster_ts import ClusterTs as cs

class Kmean(cs):
    """
    Classe de partitionnement des donnees avec l'algorithm K-mean

    Parameters:
        * ss : SeriesSupp
            instance du manager de series temporelles

    Variables:
        * seed: int
            Valeur d'initialisation de l'algo, random.
        * counter: Counter
            repartition des objets au sein des clusters
        * km: TimeSeriesKMeans
            Instance de l'algo
        * clust_name: String
            Nom de l'algo(affichage des plots)
        * metric: String
            Choix du metrics utilise, principalement softdtw ici car tres efficace et rapide
    """
    def __init__(self, ss):
        super().__init__(ss)
        self.seed = 0
        np.random.seed(self.seed)
        self.counter = None
        self.km = None
        self.clust_name = "Kmean"
        self.metric = "softdtw"

    def k_init(self, v = True):
        """
        initialisation de l'instance de l'algorithm avec les parametres actuels

        Parameters:
            * v: boolean
                Verbose, affiche les info lie au partitionnement

        Returns:
            NA
        """
        self.km = TimeSeriesKMeans(n_clusters = self.n, metric = self.metric, metric_params = {"gamma_sdtw": .01}, verbose = v, random_state = self.seed)

    def k_fit(self):
        """
        Effectue le partitionnement

        Parameters:
            NA

        Returns:
            NA
        """
        self.ts_clust = self.km.fit_predict(self.ts)

    def cluster_counter(self):
        """
        Compte les objets au sein des clusters

        Parameters:
            NA

        Returns:
            NA
        """
        self.counter = Counter(self.ts_clust)
