import pandas as pd
from os import listdir
from os.path import isfile, join
import os

class DataFactory:
    """
    Factory fournis et importe les donnees en gerant le nombre d'intances
    """

    path_GW = "csv_prepro\GW"
    path_RG24 = "csv_prepro\RG\precipiation_RG"
    path_RG1 = "csv_prepro\RG\precipitation_1h_RG"

    def __init__(self, cwd):
        """
        self.RG24 = None    [STRING]Chemin pour recuperer les donnees RG24
        self.RG1 = None     [STRING]Chemin pour recuperer les donnees RG1
        self.GW = None      [STRING]Chemin pour recuperer les donnees GW
        self.cwd = cwd      [STRING]Current working Directory

        RG24: Rain gauge, precipitation de pluie journaliere
        RG1: Rain gauge, precipitation de pluie horaire
        GW: Grand Water, donnees piezometric
        """
        self.RG24 = None
        self.RG1 = None
        self.GW = None
        self.cwd = cwd

    def get_data(self, name):
        """
        Appel la bonne methode selon name
        name: [STRING] nom des donnees associe a une instance SeriesSUpp
        """
        if name == "RG24":
            return self.get_RG24()
        if name == "RG1":
            return self.get_RG1()
        if name == "GW":
            return self.get_GW()

    def get_RG24(self):
        """
        Retourne un [DICT] en guise de dataset
        instancie une seule fois le dataset
        """
        if self.RG24 == None:
            self.RG24 = self.get_dataset(DataFactory.path_RG24)
            return self.RG24
        else:
            return self.RG24

    def get_RG1(self):
        if self.RG1 == None:
            self.RG1 = self.get_dataset(DataFactory.path_RG1)
            return self.RG1
        else:
            return self.RG1

    def get_GW(self):
        if self.GW == None:
            self.GW = self.get_dataset(DataFactory.path_GW)
            return self.GW
        else:
            return self.GW


    def get_dataset(self, source):
        """
        Recupere et retourne un Dictionnaire de Dataframe importe de multiple fichiers csv
        source: [STRING] Chemin vers les fichiers csv
        """
        all_files = [f for f in listdir(self.cwd +"\\"+ source) if isfile(join(self.cwd +"\\"+ source, f))]
        dataset = {}
        dtypes = {'Date': 'str', 'Valeur': 'float'}
        parse_dates = ['Date']
        for txt in all_files:
            data_tmp = pd.read_csv(self.cwd +"\\"+ source + "\\" + str(txt), sep=";", dtype=dtypes, parse_dates=parse_dates)
            dataset[str(txt[:-4])] = data_tmp
        print("Load " + str(source) + ": Done")
        return dataset
