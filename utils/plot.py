from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.offline.offline import _plot_html
import plotly.graph_objs as go

import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import matplotlib

import math as m
import numpy as np
class Plot:
    """
    Classe permetant l'affichage sous forme de graph de donnees
    """
    def __init__(self, cluster):
        """
        self.mode = "markers"       [STRING]Affichage des graphs Scatter (ligne, point ou ligne+point)
        self.cluster = cluster      [ClusterTs] Instance possedant en variable l'instance de Plot
        """
        self.mode = "markers"
        self.cluster = cluster

    def change_mode(self, m):
        if m == 1:
            self.mode = "markers"
        elif m == 2:
            self.mode = "lines"
        elif m == 3:
            self.mode = "markers+lines"

    def plot_cluster(self):
        """
        Methode d'affichage graphique des clusters formes par l'instance ClusterTs
        Affiche chaque groupe avec une difference de couleur pour le prototype
        """
        #colors = matplotlib.colors.cnames.copy()
        all_group_trace = {}
        colors_gathered = ["lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "lightgray" "lightgray", "lightgray", "lightgray"]
        for i in range(0, self.cluster.n):
            all_group_trace[i] = []
            if self.cluster.from_save:
                trc = self.cluster.proto[i].ravel()
            else:
                trc = self.cluster.km.cluster_centers_[i].ravel()
            index = [i for i in range(1, len(trc) + 1)]
            trace = go.Scattergl(
            x = index,
            y = trc,
            mode = str(self.mode),
            name = str("proto"),
            marker = dict(color = "red")
            )
            all_group_trace[i].append(trace)
        i = 0
        for series in self.cluster.ts:
            trc = series.ravel()
            index = [i for i in range(1, len(trc) + 1)]
            trace = go.Scattergl(
            x = index,
            y = trc,
            mode = str(self.mode),
            name = str(self.cluster.capteurs_names[i]),
            marker = dict(color = colors_gathered[self.cluster.ts_clust[i]])
            )
            all_group_trace[self.cluster.ts_clust[i]].append(trace)
            i += 1

        for i in range(0, self.cluster.n):
            fig = dict(data=all_group_trace[i],layout = {
                    'xaxis': {'title': 'Le temps'},
                    'yaxis': {'title': "La valeur"}
                    })
            #plt.subplot(self.cluster.n//2 ,2 , i + 1)
            iplot(fig)

    def plot_cluster_light(self):
        """
        Version legere d'affichage pour limiter la consommation de puissance d'un affichage dynamique
        """
        rcParams['figure.figsize'] = 20, 15
        size_of = m.ceil(self.cluster.n / 3)
        plt.figure()
        for yi in range(self.cluster.n):
            plt.subplot(size_of, 3, yi + 1)
            for xx in self.cluster.ts[self.cluster.ts_clust == yi]:
                plt.plot(xx.ravel(), "k-", alpha=.2)
            if self.cluster.from_save:
                plt.plot(self.cluster.proto[yi].ravel(), "r-")
            else:
                plt.plot(self.cluster.km.cluster_centers_[yi].ravel(), "r-")
            plt.xlim(0, self.cluster.sampler)
            plt.ylim(-4, 4)
            if yi == 1:
                plt.title(self.cluster.clust_name)
        plt.tight_layout()
        plt.show()

    def plot_scatter(self, data):
        """
        Afficha des donnees avant cluster, permet de visualiser les donnees decoupe par exemple
        data: [DICT] les donnees key: Capteur value: Dataframe
        """
        all_trace = []
        for key, value in data.items():
            trace = go.Scattergl(
            x = value["Date"],
            y = value["Valeur"],
            mode = str(self.mode),
            name = str(key)
            )
            all_trace.append(trace)

        fig = dict(data=all_trace,layout = {
                'xaxis': {'title': 'Le temps'},
                'yaxis': {'title': "La valeur"}
                })
        iplot(fig)

    def plot_scatter_by_capteur(self, data, capteur):
        all_trace = []
        for cpt in capteur:
            trace = go.Scattergl(
            x = data[cpt]["Date"],
            y = data[cpt]["Valeur"],
            mode = str(self.mode),
            name = str(str(cpt))
            )
            all_trace.append(trace)
        fig = dict(data=all_trace,layout = {
                'xaxis': {'title': 'Le temps'},
                'yaxis': {'title': "La valeur"}
                })
        iplot(fig)

    def plot_histo(self, n):
        """
        Affcihe par cluster le nombre d'occurence des Capteurs de et la granularite maximale
        """
        x0 = self.cluster.nb_capteur[n]
        x1 = self.cluster.nb_week[n]

        trace1 = go.Histogram(
            x=x0,
            opacity=0.75
        )
        trace2 = go.Histogram(
            x=x1,
            opacity=0.75
        )

        data = [trace1, trace2]
        layout = go.Layout(barmode='overlay')
        fig = go.Figure(data=data, layout=layout)

        iplot(fig, filename='overlaid histogram')

    def plot_scatter_light(self, data):
        """
        Encore une version plus legere de la methode de base
        data: [DICT] les donnees key: Capteur value: Dataframe
        """
        rcParams['figure.figsize'] = 15, 6
        colors = matplotlib.colors.cnames.copy()
        for key, value in data.items():
            df = value.set_index("Date")
            df = pd.to_numeric(df.Valeur)
            trc = plt.plot(df, color=colors.popitem()[0],label = key)
        plt.legend(loc=2)
        plt.title('Light TS plot')
        plt.show(block=False)

    def plot_simple_list(self, list):
        for elmt in list:
            plt.plot(elmt)
