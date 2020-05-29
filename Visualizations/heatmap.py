<<<<<<< HEAD
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage.filters as filters
from PIL import Image
from bokeh.plotting import figure, output_file, show

data = pd.read_csv(r"C:/Users/20191071/Desktop/MetroMapsEyeTracking/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv"
                   ,encoding = "latin1",delim_whitespace=True)

output_file('image.html', mode='inline')

stimuli = '01_Antwerpen_S1.jpg'
stimuli_url = '/Users/20191071/Desktop/MetroMapsEyeTracking/MetroMapsEyeTracking/stimuli/01_Antwerpen_S1.jpg'

stimuli_filter = data['StimuliName'] == stimuli
mapped = data[stimuli_filter]
ds = data[data['StimuliName'] == stimuli].reset_index().copy()

#image size
img = Image.open(stimuli_url)
width, height = img.size

io = plt.imread(stimuli_url)
i = io.copy().astype(np.uint8)  #cast numpy array to specific type: Unsigned integer (0 to 255)

if i.ndim == 2: #number of dimensions of array
    i = cv2.cvtColor(i, cv2.COLOR_GRAY2RGBA) #color gray
else:
    if i.ndim == 3:
        i = cv2.cvtColor(i, cv2.COLOR_RGB2RGBA) #color from RGB

i = np.flipud(i) ##flips array in the up/down direction

#check is the point is inside the bounds
bounds = (ds['MappedFixationPointX']>width) | (ds['MappedFixationPointY']>height) \
         | (ds['MappedFixationPointX']<0) | (ds['MappedFixationPointY']<0)

ds = ds[np.logical_not(bounds)].reset_index().copy()

#create numpy arrays for fixation point x, fixation point y and fixation duration
point_x = np.array([])
point_y = np.array([])
duration = np.array([])

for index, row in ds.iterrows():
    point_x = np.append(point_x, np.array([row['MappedFixationPointX']]))
    point_y = np.append(point_y, np.array([row['MappedFixationPointY']]))
    duration = np.append(duration, np.array([row['FixationDuration']]))

#create histogram H using numpy histogram 2d
H, x_edges, y_edges = np.histogram2d(point_y, point_x, bins=200, weights=duration)
H = filters.gaussian_filter(H, sigma=4)  #gaussian filter
H = np.flipud(H)  #flips array in the up/down direction

#map the heatmap
p = figure(plot_width=900, plot_height=700, x_range=(0, width), y_range=(height, 0))
p.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)
p.image(image=[H], x=0, y=height, dw=width, dh=height, palette="Turbo11", global_alpha=0.5)

show(p)
=======
from IPython.display import Image
import numpy as np
import pandas as pd
import matplotlib.image
# next command ensures that plots appear inside the notebook
import matplotlib as mpl
import matplotlib.pyplot as plt
from bokeh.models import ColorBar, LogColorMapper, LogTicker
from bokeh.plotting import figure, output_file, show
from scipy.ndimage.filters import gaussian_filter

image=mpimg.imread('./stimuli/01_Antwerpen_S1.jpg')
data=pd.read_csv('all_fixation_data_cleaned_up.csv',encoding = "latin1",delim_whitespace=True)

x=mapped['MappedFixationPointX']
y=mapped['MappedFixationPointY']

height, width, c = image.shape

s=64
def myplot(x, y, s, bins=users):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(width, height))
    heatmap = gaussian_filter(heatmap, sigma=s)
    

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent
fig3, axes = plt.subplots(nrows=1,ncols=1,figsize=(20,20))
axes.imshow(image, extent=[0, width, 0, height])
s=64
img, extent = myplot(x, y, s)

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


axes.imshow(img, extent=extent, cmap="Test")

plt.xlim(0, width)
plt.ylim(0, height)
plt.show()

>>>>>>> parent of d01ca04... Heatmap visualizations modified
