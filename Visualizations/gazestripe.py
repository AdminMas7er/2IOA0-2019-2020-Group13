import pandas as pd
import random
import numpy as np
from PIL import Image
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import turbo
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

data = pd.read_csv("/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace = True)

output_file('image.html', mode="inline")

stimuli = '02_Berlin_S1.jpg'
stimuli_url = '/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/stimuli/02_Berlin_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

user_array=mapped['user'].unique()

img =  Image.open(stimuli_url)
width, height = img.size

p = figure(plot_width = 900, plot_height=700, x_range=(0,width), y_range=(height,0))

#p.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)

#box is in format of (x1, y1, x2, y2) - x1y1 are top left and x2y2 are bottom right

box = (155, 65, 360, 270)
img1 = img.crop(box)

#img1.show()

img = plt.imread(stimuli_url)

fig, ax = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, squeeze=False)
ax[0,0].imshow(img)
ax[0,1].imshow(img)
ax[0,2].imshow(img)
ax[0,0].axis('off')
ax[0,1].axis('off')
ax[0,2].axis('off')

ax[1,0].imshow(img)
ax[1,1].imshow(img)
ax[1,2].imshow(img)
ax[1,0].axis('off')
ax[1,1].axis('off')
ax[1,2].axis('off')

fig.subplots_adjust(wspace=0, hspace=0)

plt.show()

#imgplot = plt.imshow(img)
