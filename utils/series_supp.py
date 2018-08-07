import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from math import sqrt
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
date_parser = pd.to_datetime

class SeriesSupp:
    """Premet d'organiser et de manipuler les données.

    Parameters:
        * cwd: String
            chemin d'acces ou le main est excecute
        * factory: Factory
            Instance de la factory
        * dataset_name: String
            Definie le type de donnees a recuperer

    Variables:
        * dataset: {Dict}
            Le dataset original sans modification
        * tmp_dataset: {Dict}
            Le dataset actuel avec les modification
        * years: [ARRAY<STRING>]
            Setup de decoupage par annees
        * months: [ARRAY<STRING>]
            Setup de decoupage par mois
        * days: [ARRAY<STRING>]
            Setup de decoupage par annees | [BOOL] decoupage semaines
        * factory: DataFactory
            Instance de la Factory
        * dataset_name: String
            Permet de connaitre la source souhaite e.g import_dataset()

    """
    def __init__(self, cwd, factory, dataset_name):
        self.cwd = cwd
        self.dataset = {}
        self.tmp_dataset = {}
        self.years = []
        self.months = []
        self.days = False
        self.factory = factory
        self.norm = False
        self.rounded = False
        self.smoothed = False
        self.dataset_name = dataset_name
        self.reset_years()

    def __repr__(self):
        """ Representation de l'instance """
        return str("Dataset: " + str(self.dataset_name) + ". De taille source: " + str(len(self.dataset)) + ". et de taille current: " + str(len(self.tmp_dataset)))

    def reset_years(self):
        """Par defaut decoupe les TS dans la granularite maximale"""
        self.years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
    def reset_months(self):
        """Par defaut decoupe les TS dans la granularite maximale"""
        self.months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    def reset_days(self):
        """Par defaut decoupe les TS dans la granularite maximale"""
        self.days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

    def reset_dataset(self):
        """ Retourne aux donnees importes avant modifications """
        reset = self.dataset.copy()
        self.tmp_dataset = reset
        self.norm = False
        self.days = False

    def reset_setup(self):
        """ Full reset des variables de granularites """
        self.reset_years()
        self.reset_months()
        self.reset_days()

    def info(self):
        """ Permet d'avoir une idees des donnees du dataset en prenant une TS au hasard"""
        k, v = next(iter(self.dataset.items()))
        print("Taille du dataset dictionnaire: " + str(len(self.dataset)))
        print("Capteur: " + k)
        print(v.info())
        print(v.head())
        print(v.tail())

    def get_data(self):
        """ Getter du dataset modifie """
        return self.tmp_dataset.copy()

    def import_dataset(self):
        """ Appel a la factory pour recuperer les donnees """
        self.dataset = self.factory.get_data(self.dataset_name)
        self.reset_dataset()

    def smooth(self, data, wind, col):
        """
        Smooth via rolling window

        Parameters:
            * data: DataFrame
                La DF a smooth, attention a bien choisir la colonne voulu
            * wind: int
                Taille de fentre
            * col: String
                La colonne de la DF a smooth

        Returns:
            data: DataFrame
                La DF remanie
        """
        data[col] = data[col].rolling(window = wind, center = True).mean()
        data = data.drop(list(range(len(data) - wind,len(data))))
        data = data.drop(list(range(wind)))
        data.reset_index()
        return data

    def dict_smooth(self, wind = 24, col = "Valeur"):
        """
        Dictionnaire full smooth

        Parameters:
            * wind: int
                Taille de la fenetre 24 pour smooth journalier
            * col: str (DEFAUlT = "Valeur")
                Colonne cible de l'action
        Returns:
            NA
        """
        res = {}
        tampon = self.tmp_dataset.copy()
        for k, v in tampon.items():
            tampon_v = v.copy()
            res[k] = self.smooth(data = tampon_v, wind = wind, col = col)
        self.tmp_dataset = res
        self.smoothed = True

    def normalize(self, data):
        """
        Normalisation des TS, moyenne: 0 et ecart type: 1
        Data: dataframe
        """
        # prepare data for standardization
        values = data.loc[:,("Valeur")]
        values_r = values.values.reshape((len(values), 1))
        # train the standardization
        scaler = StandardScaler()
        scaler = scaler.fit(values_r)
        tr_v = scaler.transform(values_r)
        data["Valeur"] = tr_v
        return data

    def standardize(self, data):
        """
        Standardize des TS, moyenne: 0 et ecart type: 1
        Data: dataframe
        """
        # prepare data for standardization
        values = data["Valeur"]
        values = values.values.reshape((len(values), 1))
        # train the standardization
        t = TimeSeriesScalerMeanVariance().fit_transform(values)
        print(t)
        data["valeur"] = TimeSeriesScalerMeanVariance().fit_transform(values)
        return data

    def dict_round(self):
        """ Normalise un dictionnaire de TS """
        for k, v in self.tmp_dataset.items():
            #print(v.shape)
            v = self.rounding(v)
        self.rounded = True

    def dict_norm(self):
        """ Normalise un dictionnaire de TS """
        for k, v in self.tmp_dataset.items():
            #print(v.shape)
            v = self.normalize(v)
        self.norm = True

    def dict_stand(self):
        """ Normalise un dictionnaire de TS """
        for k, v in self.tmp_dataset.items():
            #print(v.shape)
            v = self.standardize(v)
        self.norm = True

    def split_data_years(self):
        """ Decoupage des TS selon la variable d'annees """
        res = {}
        for y in self.years:
            for k, v in self.tmp_dataset.items():
                v = v.set_index("Date")
                try:
                    tmp = v[v.index.year == y]
                    v = v.reset_index()
                    tmp = tmp.reset_index()
                    if tmp.shape[0] != 0:
                        res[str(k) + "_" + str(y) ] = tmp
                except KeyError:
                    print(k + ": pas de données en " + str(y))
        if len(res) != 0:
            self.tmp_dataset = res

    def split_data_months(self):
        """ Decoupage des TS selon la variable de mois """
        res = {}
        for m in self.months:
            for k, v in self.tmp_dataset.items():
                v = v.set_index("Date")
                try:
                    tmp = v[v.index.month == m]
                    v = v.reset_index()
                    tmp = tmp.reset_index()
                    if tmp.shape[0] != 0:
                        if len(str(m)) == 1:
                            ret_m = "0"+str(m)
                        else:
                            ret_m = m
                        res[str(k) + "_" + str(ret_m) ] = tmp
                except KeyError:
                    print(k + ": pas de données en " + str(m))
        if len(res) != 0:
            self.tmp_dataset = res

    def split_data_weeks(self):
        """ Decoupage des TS selon les semaines"""
        res = {}
        for k, v in self.tmp_dataset.items():
            tmp = v.groupby(pd.Grouper(key='Date', freq='W'))
            for i in tmp:
                if i[1].shape[0] != 0:
                    if len(str(i[0].week)) == 1:
                        ret_d = "0"+str(i[0].week)
                    else:
                        ret_d = i[0].week
                    res[str(k) + "_" + str(ret_d) ] = i[1]
        if len(res) != 0:
            self.tmp_dataset = res
            self.days = True

    def split_all(self):
        self.split_data_years()
        self.split_data_months()
        if self.days:
            self.split_data_weeks()

    def get_data_from_captor(self, cpt):
        """
        Retourne toutes les series temporelles liees a un nom de capteur

        Parameters:
            * cpt: String
                Nom du capteur desire

        Returns:
            res: {Dict}
                Sous dataset du capteur associe, les clefs sont les differente declinaisons en series temporelles du capteur, varie en longueur selon la granularite
        """
        res = {}
        for k, v in self.tmp_dataset.items():
            if cpt in k:
                res[k] = v
        return res

 ################################################# For precise split where each captor don't compare to itself #################################################
    def split_year_multi_month(self):
        res = {}
        for k, v in self.tmp_dataset.items():
            v = v.set_index("Date")
            tmp = pd.DataFrame({'A' : []})
            try:
                for m in self.months:
                    if tmp.empty:
                        tmp = v[self.year +"-"+ m]
                    else:
                        tmp = pd.concat([tmp, v[self.year +"-"+ m]])
                tmp = tmp.reset_index()
                res[k] = tmp
            except KeyError:
                print(k + ": pas de données en " + self.year +"-"+ str(m))
        self.tmp_dataset = res

    def split_year_month_multi_day(self, dataset, month):
        res = {}
        for k, v in dataset.items():
            v = v.set_index("Date")
            tmp = pd.DataFrame({'A' : []})
            try:
                for d in self.days:
                    if tmp.empty:
                        tmp = v[self.year +"-"+ month + "-" + d]
                    else:
                        tmp = pd.concat([tmp, v[self.year +"-"+ month + "-" + d]])
                tmp = tmp.reset_index()
                res[k] = tmp
            except KeyError:
                print(k + ": pas de données en " + self.year +"-"+ month + "-" + d)
        return res

    def split_year_multi_month_multi_day(self):
        res = {}
        for k, v in self.tmp_dataset.items():
            v = v.set_index("Date")
            tmp = pd.DataFrame({'A' : []})
            for m in self.months:
                for d in self.days:
                    if tmp.empty:
                        try:
                            tmp = v[str(self.year) +"-"+ m + "-" + d]
                        except KeyError:
                            print(k + ": pas de données en " + self.year +"-"+ m +"-"+ d)
                    else:
                        try:
                            tmp = pd.concat([tmp, v[str(self.year) +"-"+ m +"-"+ d]])
                        except KeyError:
                            print(k + ": pas de données en " + self.year +"-"+ m +"-"+ d)
            tmp = tmp.reset_index()
            res[k] = tmp
        self.tmp_dataset = res

    def split_each_steps(self):
        res = {}
        if not self.months:
            self.reset_months()
        if not self.days:
            self.reset_days()

        for k, v in self.tmp_dataset.items():
            v = v.set_index("Date")
            tmp = pd.DataFrame({'A' : []})
            for y in self.years:
                for m in self.months:
                    for d in self.days:
                        pass
