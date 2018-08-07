class Parser:
    """
    Transforme les donnees d'un format a un autre a l'aide de methodes de transformations
    """
    def __init__(self):
        pass

    def sax_to_spmf(self, data, separator = False):
        """
        Du format SAX au format SPMF(un soft de data mining avec son propre format)

        Parameters:
            * data: SAX

        Returns:
            res_str: String
        """
        res_str = ""
        for itemset in data:
            tmp_str = ""
            tmp_itemset = itemset.ravel()
            for item in tmp_itemset:
                tmp_str += str(item)
                tmp_str += " "
            if separator:
                tmp_str += "-1#"
            else:
                tmp_str += "-1 "
            res_str += tmp_str
        res_str += "-2"
        return res_str
