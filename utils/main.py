import os
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.offline.offline import _plot_html
import plotly.graph_objs as go
print (__version__) # requires version >= 1.9.0
init_notebook_mode(connected=True)

from mpl_toolkits import mplot3d
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
#%matplotlib notebook
#%matplotlib inline
from utils import series_supp as ss
from utils import data_factory as df
from utils import k_mean as km

class Main:

    def __init__(self, cwd):
        self.cwd = cwd
        os.chdir(cwd)
        self.factory = df.DataFactory(cwd)
        self.store_path = "cluster\\"

        self.RG24 = ss.SeriesSupp(cwd, factory, "RG24")
        self.RG1 = ss.SeriesSupp(cwd, factory, "RG1")
        self.GW = ss.SeriesSupp(cwd, factory, "GW")
