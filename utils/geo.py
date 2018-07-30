from mpl_toolkits import mplot3d
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from scipy.spatial.distance import squareform, pdist
from plotly.offline.offline import _plot_html
import plotly.graph_objs as go
from matplotlib.pylab import rcParams
import pandas as pd
import numpy as np

class Geo:
    """
    Classe entièrement dedie a l'affichage des capteur dans l'espace les donnees sont normees suivant un type de geolocalisation geologique
    propre a la NC, la classe dispose de plusieurs type d'affichage

    Parameters:
        cwd: String
            Chemin vers le main

    Variables:
        path_geo_RG: String
            Chemin pour recuperer les donnees RG
        path_geo_GW: String
            Chemin pour recuperer les donnees GW
        geo_RG: {Dict}
            Les donnees geo_RG
        geo_GW: {Dict}
            Les donnees geo_GW
        dist_mat: pandas.DataFrame
            Matrice des distances entre les pluviometre et des piezometres

    Notes:
        RG: Rain gauge, precipitation de pluie journaliere
        GW: Grand Water, donnees piezometric
    """
    def __init__(self, cwd):
        self.cwd = cwd
        self.path_geo_RG = "geo\geo_RG.txt"
        self.path_geo_GW = "geo\geo_GW.txt"
        self.geo_GW = self.get_geo_data(self.path_geo_GW)
        self.geo_RG = self.get_geo_data(self.path_geo_RG)
        self.dist_mat = None

    def get_geo_data(self, source):
        """
        Recupere les donnees geographique

        Parameters:
            source: String
                location ou recuperer ces donnees

        Returns:
            data: pandas.DataFrame
                Donnees sous forme de tableau
        """
        data = pd.read_csv(self.cwd +"\\"+ source, sep=";")
        return data

    def highlight_min(self, s):
        """
        Parametre d'affichage surligne les min par ligne de DataFrame

        Parameters:
            s: pandas
                Ligne du tableau

        Returns:
            unnamed: pands.style
                Affichage des min
        """
        is_min = s == s.min()
        return ['background-color: lightgreen' if v else '' for v in is_min]

    def distance_matrix(self):
        """
        Retourne une dataframe representant les distances entre piezo et pluvio ainsi que les distances les plus courte

        Parameters:
            NA

        Returns:
            gdist_style: pandas.style
                Matrice stylise des distances
        """
        ggw = self.geo_GW.copy()
        gwlist = ggw["capteur"]
        grg = self.geo_RG.copy()
        rglist = grg["capteur"]
        g = pd.concat([ggw, grg])

        gdist = pd.DataFrame(squareform(pdist(g.iloc[:, 1:])), columns= g.capteur.unique(), index= g.capteur.unique()).round(1)
        gdist = gdist.drop(columns = gwlist)
        gdist = gdist.drop(index = rglist)

        self.dist_mat = gdist

        gdist_style = gdist.style.apply(self.highlight_min, axis = 1)
        return gdist_style

    def distance_dict(self):
        res = {}
        for col in self.dist_mat:
            res[col] = []
        #for index, row in self.dist_mat.iteritems():
        #for index, row in self.dist_mat.iterrows():
        for row in self.dist_mat.itertuples():
            xmin = min(row[1:])
            for k, v in row._asdict().items():
                if v == xmin:
                    key = k
            res[key].append(row._asdict()["Index"])
        #print(res)
        self.distance_dict = res
            #for elmt in row:
            #    print(elmt)
            #print(min(row))
            #print(self.dist_mat.columns[index, min(row)])
            #res[?].append(index)

    def plot_3D (self):
        """
        Afficha 3D des geolocalisations des ouvrages

        Parameters:
            NA

        Returns:
            NA
        """
        rcParams['figure.figsize'] = 8, 6
        fig = plt.figure()
        #ax = plt.scatter(projection='3d')
        ax = fig.add_subplot(111, projection='3d')
        # Data for a three-dimensional line
        zlineG = self.geo_GW["alt"]
        xlineG = self.geo_GW["lon"]
        ylineG = self.geo_GW["lat"]
        #ax.plot3D(xlineG, ylineG, zlineG, 'red')
        ax.scatter(xlineG, ylineG, zlineG, c='red')

        zlineR = self.geo_RG["alt"]
        xlineR = self.geo_RG["lon"]
        ylineR = self.geo_RG["lat"]
        #ax.plot3D(xlineR, ylineR, zlineR, 'blue')
        ax.scatter(xlineR, ylineR, zlineR, c='blue')

    def plot_3D_for_all_cluster(self, names): #Besoin de faire un fois unique pour chaque capteur appartenant à chaque cluster. names[DICT]
        rcParams['figure.figsize'] = 8, 6
        fig = plt.figure()
        #ax = plt.scatter(projection='3d')
        ax = fig.add_subplot(111, projection='3d')
        colors = ["g", "r", "c", "y", "m", "k"]
        for k, v in names.items():
            # Data for a three-dimensional line
            tmp = self.geo_GW[~self.geo_GW["capteur"].isin(v)]
            zlineG = tmp["alt"]
            xlineG = tmp["lon"]
            ylineG = tmp["lat"]
            #ax.plot3D(xlineG, ylineG, zlineG, 'red')
            ax.scatter(xlineG, ylineG, zlineG, c=colors[k])

        zlineR = self.geo_RG["alt"]
        xlineR = self.geo_RG["lon"]
        ylineR = self.geo_RG["lat"]
        #ax.plot3D(xlineR, ylineR, zlineR, 'blue')
        ax.scatter(xlineR, ylineR, zlineR, c='blue')

    def plot_3D_for_one_cluster(self, names): #names[liste]
        rcParams['figure.figsize'] = 8, 6
        fig = plt.figure()
        #ax = plt.scatter(projection='3d')
        ax = fig.add_subplot(111, projection='3d')
        # Data for a three-dimensional line
        tmp = self.geo_GW[~self.geo_GW["capteur"].isin(names)]
        zlineG = tmp["alt"]
        xlineG = tmp["lon"]
        ylineG = tmp["lat"]
        #ax.plot3D(xlineG, ylineG, zlineG, 'red')
        ax.scatter(xlineG, ylineG, zlineG, c='k')

        tmp = self.geo_GW[self.geo_GW["capteur"].isin(names)]
        zlineG = tmp["alt"]
        xlineG = tmp["lon"]
        ylineG = tmp["lat"]
        #ax.plot3D(xlineG, ylineG, zlineG, 'red')
        ax.scatter(xlineG, ylineG, zlineG, c='r')

        zlineR = self.geo_RG["alt"]
        xlineR = self.geo_RG["lon"]
        ylineR = self.geo_RG["lat"]
        #ax.plot3D(xlineR, ylineR, zlineR, 'blue')
        ax.scatter(xlineR, ylineR, zlineR, c='blue')

    def plotly_3D(self, names):
        """
        Afficha 3D des geolocalisations des ouvrages avec plotly cette fois
        Plus utilise que le premier

        Parameters:
            names: String
                Nom des capteurs pour les afficher au survol

        Returns:
            NA
        """
        tmp = self.geo_GW[~self.geo_GW["capteur"].isin(names)]
        tmp_names = []
        for index, row in tmp.iterrows():
            tmp_names.append(row["capteur"])
        zlineG = tmp["alt"]
        xlineG = tmp["lon"]
        ylineG = tmp["lat"]
        GW_out = go.Scatter3d( # Trace les non compris dans le cluster
            x=xlineG,
            y=ylineG,
            z=zlineG,
            mode='markers',
            name="Capteurs non inclus",
            #customdata=["test1"],
            hovertext=tmp_names,
            marker=dict(
                color='rgb(0, 0, 0)',
                size=12,
                symbol='circle',
                line=dict(
                    color='rgb(255, 255, 255)',
                    width=1
                ),
                opacity=0.9
            )
        )
        tmp = self.geo_GW[self.geo_GW["capteur"].isin(names)]
        tmp_names = []
        for index, row in tmp.iterrows():
            tmp_names.append(row["capteur"])
        zlineG = tmp["alt"]
        xlineG = tmp["lon"]
        ylineG = tmp["lat"]
        GW_in = go.Scatter3d( # Trace les compris dans le cluster
            x=xlineG,
            y=ylineG,
            z=zlineG,
            mode='markers',
            name="Capteurs inclus",
            #customdata=["test2"],
            hovertext=tmp_names,
            marker=dict(
                color='rgb(255, 0, 0)',
                size=12,
                symbol='circle',
                line=dict(
                    color='rgb(0, 0, 0)',
                    width=1
                ),
                opacity=0.9
            )
        )
        tmp_names = []
        for index, row in self.geo_RG.iterrows():
            tmp_names.append(row["capteur"])
        zlineR = self.geo_RG["alt"]
        xlineR = self.geo_RG["lon"]
        ylineR = self.geo_RG["lat"]

        Pluviometre = go.Scatter3d( # Trace les pluviometres
            x=xlineR,
            y=ylineR,
            z=zlineR,
            mode='markers',
            name="Pluviometres",
            #customdata=["test3"],
            hovertext=tmp_names,
            marker=dict(
                color='rgb(0, 255, 0)',
                size=12,
                symbol='circle',
                line=dict(
                    color='rgb(0, 0, 0)',
                    width=1
                ),
                opacity=0.9
            )
        )
        data = [GW_out, GW_in, Pluviometre]
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=data, layout=layout)
        iplot(fig, filename='simple-3d-scatter')

    def plot_2D(self):
        trace_GW = go.Scattergl(
        x = self.geo_GW["lon"],
        y = self.geo_GW["lat"],
        mode = "markers",
        name = "GW",
        marker = dict(size = self.geo_GW["alt"]),
        text= self.geo_GW["capteur"]
        )

        trace_RG = go.Scattergl(
        x = self.geo_RG["lon"],
        y = self.geo_RG["lat"],
        mode = "markers",
        name = "RG",
        marker = dict(size = self.geo_RG["alt"]),
        text= self.geo_RG["capteur"]
        )

        fig = dict(data=[trace_GW, trace_RG], layout = {
                'xaxis': {'title': 'Lon'},
                'yaxis': {'title': "Lat"}
                })

        iplot(fig)

    def get_minrange_rg(self, cpt):
        true_cpt = cpt[:2]
        true_cpt += cpt[3:]
        res = ""
        for k, v in self.distance_dict.items():
            if true_cpt in v:
                res = k
        if res == "":
            res = "RG007"
        return res
