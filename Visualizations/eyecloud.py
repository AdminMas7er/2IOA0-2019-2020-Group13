import numpy as np
import pandas as pd
import random

from PIL import Image, ImageDraw
from bokeh.models import ColumnDataSource
from bokeh.palettes import turbo
from bokeh.plotting import figure, output_file, show
from sklearn.cluster import KMeans

output_file("image.html", mode='inline')

data = pd.read_csv('C:/Users/20190825/Desktop/TUE NOTES/2IOA0/MetroMapsEyeTracking/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace = True)

stimuli = '01_Antwerpen_S1.jpg'
stimuli_url = 'C:/Users/20190825/Desktop/TUE NOTES/2IOA0/MetroMapsEyeTracking/MetroMapsEyeTracking/stimuli/01_Antwerpen_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

img_rgba =  Image.open(stimuli_url)


Cluster_map=mapped[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].copy()

km=KMeans(n_clusters=3)
km.fit(Cluster_map)
centers=pd.DataFrame(km.cluster_centers_,columns=Cluster_map.columns)
centers_coords=centers[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].itertuples(index=False,name=None)
centre_pairs=list(centers_coords)

cropped_thumbs=[]

for x,y,size in centre_pairs:
    box=((x-size/2,y-size/2,x+size/2,y+size/2))
    im_a=Image.new("L",img_rgba.size,0)
    draw=ImageDraw.Draw(im_a)
    draw.ellipse(box)
    im_rgba=img_rgba.copy()
    im_rgba.putalpha(im_a)
    im_rgba_crop=im_rgba.crop(box)
    cropped_thumbs.append(np.array(im_rgba_crop).view(np.uint32)[::-1])
centers['thumbnails']=cropped_thumbs
ds=ColumnDataSource(centers)
img_size=1
plot_gazeplot = figure(plot_width =1000 , plot_height=700, match_aspect=True)
plot_gazeplot.image_rgba(image='thumbnails', x='MappedFixationPointX', y='MappedFixationPointY', dw=img_size, dh=img_size, source=ds)



plot_gazeplot.xgrid.visible = False
plot_gazeplot.ygrid.visible = False


show(plot_gazeplot)
