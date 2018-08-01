
class Parser:
    def __init__(self):
        pass

    def sax_to_spmf(self, data, separator = False):
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
