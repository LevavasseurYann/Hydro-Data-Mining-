from tslearn.clustering import TimeSeriesKMeans
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, TimeSeriesResampler
from tslearn.utils import to_time_series
from tslearn.utils import to_time_series_dataset
from utils.plot import Plot
from utils.geo import Geo
import pickle

class ClusterTs:
    """
    Classe mere permettant de gerer et modifier les donnees afin de les clusteriser
    """
    def __init__(self, ss):
        self.ts = None
        self.ts_clust = None
        self.ts_name = None
        self.ss = ss
        self.sampler = 168 # 24/d - 168/w - 744[31](743[30]-696[29]-672[28])/m - 8760(8784)/y
        self.ploter = Plot(self)
        self.n = 5
        self.capteurs_names = []
        self.from_save = False
        self.proto = []
        self.last_readed = {}
        self.store_path = "cluster/"
        self.clust_name = "Master"
        self.metric = ""
        self.geo = Geo(self.ss.cwd)
        self.cluster_by_name = {}
        self.cluster_by_fullname = {}
        self.size_min = 0

    def __repr__(self):
        my_repr = ["Algorithm de clustering: " + self.clust_name, "Metric mesure: " + self.metric, "Espace de stockage: " + self.store_path, "Nombre de Clusters: " + str(self.n), "Sampler de taille : " + str(self.sampler)]
        return '\n'.join('%s' % v for v in my_repr)

    def tslearn_format_export(self):
        df = []
        dn = []
        for k, v in self.ss.get_data().items():
            if not self.check_equal(v["Valeur"].values):
                if len(v["Valeur"].values) > self.size_min:
                    df.append(v["Valeur"].values)
                    dn.append(k)
                    self.capteurs_names.append(k)
        df_set = to_time_series_dataset(df)
        if self.sampler != 0:
            df_set = TimeSeriesResampler(self.sampler).fit_transform(df_set)
        self.ts = df_set
        self.ts_name = dn

    def set_size_min(self, size):
        self.size_min = size

    def check_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    def store_cluster(self, name):
        info_dict = {}
        info_dict["trace"] = self.ts
        info_dict["classe"] = self.ts_clust
        info_dict["name"] = self.ts_name
        info_dict["proto"] = self.km.cluster_centers_
        info_dict["sample"] = self.sampler
        info_dict["years"] = self.ss.years
        info_dict["months"] = self.ss.months
        info_dict["days"] = self.ss.days

        outfile = open(self.store_path + name + ".pkl", "wb")
        pickle.dump(info_dict, outfile)
        outfile.close()

        file = open(self.store_path + name + ".txt", "w")
        file.write(str([i for i in self.ss.years]) + "\n")
        file.write(str([i for i in self.ss.months]) + "\n")
        file.write("Weeks split: " + str(self.ss.days) + "\n")
        file.write("Normalized: " + str(self.ss.norm) + "\n")
        file.write("Sample size(0=None): " + str(self.sampler) + "\n")
        file.write("Algorithm used: " + str(self.clust_name) + "\n")
        file.write("nb cluster: " + str(self.n) + "\n")
        file.write("Distance measure: " + str(self.metric) + "\n")
        file.close()

#    def read_cluster(self, path, name):
#        infile = open(str(path) + name + ".pkl",'rb')
#        info_dict = pickle.load(infile)
#        infile.close()
#        self.ts = info_dict["trace"]
#        self.ts_clust = info_dict["classe"]
#        self.ts_name = info_dict["name"]
#        self.capteurs_names = info_dict["name"]
#        self.proto = info_dict["proto"]
#        self.n = len(info_dict["proto"])
#        self.sampler = info_dict["sample"]
#        self.from_save = True
#        self.last_readed = info_dict
#        self.ss.years = info_dict["years"]
#        self.ss.months = info_dict["months"]
#        self.ss.days = info_dict["days"]

    def read_cluster(self, path, name):
        infile = open(str(path) + name + ".pkl",'rb')
        info_dict = pickle.load(infile)
        infile.close()
        self.ts = info_dict["trace"]
        self.ts_clust = info_dict["classe"]
        self.ts_name = info_dict["name"]
        self.capteurs_names = info_dict["name"]
        self.proto = info_dict["proto"]
        self.n = len(info_dict["proto"])
        self.sampler = info_dict["sample"]
        self.from_save = True
        self.last_readed = info_dict

    def capteur_parser(self):
        res = {}
        res_full = {}
        for i in range(0, self.n):
            res[i] = []
        for elmt in self.ts_name:
            non_parse = str(elmt)
            parse = str(elmt[0:2] + elmt[3:6])
            if parse not in res[self.ts_clust[self.ts_name.index(elmt)]]:
                res[self.ts_clust[self.ts_name.index(elmt)]].append(parse)
            res_full[self.ts_clust[self.ts_name.index(elmt)]].append(non_parse)
        self.cluster_by_name = res
        self.cluster_by_fullname = res_full
