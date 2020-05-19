from IPython.display import Image
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import imshow
from bokeh.models import ColorBar, LogColorMapper, LogTicker
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Inferno256
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter
image=mpimg.imread('./stimuli/01_Antwerpen_S1.jpg')
data=pd.read_csv('all_fixation_data_cleaned_up.csv',encoding = "latin1",delim_whitespace=True)

stimuli_filter=data['StimuliName']=='01_Antwerpen_S1.jpg'
mapped=data[stimuli_filter]
user_array=mapped['user'].unique()
user_array

fig2=plt.figure(figsize=(20,20))
x=mapped['MappedFixationPointX']
y=mapped['MappedFixationPointY']

users=mapped['user'].count()


height, width, c = image.shape
output_file("image.html")
s=64
heatmap, xedges, yedges = np.histogram2d(x, y, bins=(width, height))
#heatmap = gaussian_filter(heatmap, sigma=s)

random_colorscheme = {'red':  ((0.0, 0.0, 0.0),
                   (0.25, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (0.72, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.7, 0.8),
                   (0.25, 0.8, 0.7),
                   (0.5, 0.9, 0.9),
                   (0.88, 1.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (0.25, 0.0, 0.0),
                   (0.5, 0.1, 0.0),
                   (0.75, 0.1, 0.0),
                   (1.0, 0.3, 0.0))
        
         }
Test_alpha = random_colorscheme.copy()
Test_alpha['alpha'] = ((0.0, 0.0, 0.0),
                   (0.40,0.6,0.6),
                   (0.60, 0.7, 0.7),
                   (0.80, 0.8, 0.8),
                   (1.0, 0.8, 1.0))

plt.register_cmap(name='Test', data=Test_alpha)
palette=Inferno256


plot=figure(x_range=(0,width),y_range=(0,height))
plot.image(image=[heatmap],x=xedges[0],y=yedges[0],dw=xedges[-1]-xedges[0],dh=yedges[-1]-yedges[0])
show(plot)

#plt.xlim(0, width)
#plt.ylim(0, height)
#plt.show()

