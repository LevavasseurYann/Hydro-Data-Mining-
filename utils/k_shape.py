from tslearn.clustering import KShape
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, TimeSeriesResampler
from tslearn.utils import to_time_series
from tslearn.utils import to_time_series_dataset
from collections import Counter
import numpy as np

from utils.cluster_ts import ClusterTs as cs

class Kshape(cs):

    def __init__(self, ss):
        super().__init__(ss)
        self.seed = 0
        np.random.seed(self.seed)
        self.counter = None
        self.km = None
        self.clust_name = "Kshape"
        self.metric = "shape"

    def k_init(self, v = True):
        self.km = KShape(n_clusters = self.n, verbose = v, random_state = self.seed)

    def k_fit(self):
        self.ts_clust = self.km.fit_predict(self.ts)

    def cluster_counter(self):
        self.counter = Counter(self.ts_clust)
