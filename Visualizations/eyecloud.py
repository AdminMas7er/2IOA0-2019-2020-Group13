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

stimuli = '10_Barcelona_S1.jpg'
stimuli_url = 'C:/Users/20190825/Desktop/TUE NOTES/2IOA0/MetroMapsEyeTracking/MetroMapsEyeTracking/stimuli/10_Barcelona_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

img =  Image.open(stimuli_url)
img_rgb = img.convert('RGB') #converting the image in RGB values

Cluster_map=mapped[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].copy() #creating a separate dataframe for the clustering

km=KMeans(n_clusters=6) #number of clusters
km.fit(Cluster_map)
centers=pd.DataFrame(km.cluster_centers_,columns=Cluster_map.columns) #generating the centre of each cluster
centers_coords=centers[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].itertuples(index=False,name=None)  #putting the x, y, size values of each centre in a tuple
centre_pairs=list(centers_coords) #getting those tuples in a list

cropped_thumbs=[]
i=0
for x,y,size in centre_pairs: #generating the cricle crop by creating a separate black background with awhite circle which is the alpha channel and superimposing the RGB channel
    img_cropped=img_rgb.crop((x,y,x+size/2,y+size/2)) 
    alpha =Image.new('L',img_cropped.size)
    alpha_draw=ImageDraw.Draw(alpha)
    wc,hc=img_cropped.size
    alpha_draw.ellipse((0,0,wc,hc),fill=255)
    img_cropped.putalpha(alpha)

    cropped_thumbs.append(np.array(img_cropped).view(np.uint32)[::-1]) 
centers['thumbnails']=cropped_thumbs

centers['FixationDuration']=centers['FixationDuration']/6.25
print(centers)
ds=ColumnDataSource(centers)
plot_eyeclouds = figure(plot_width =1000 , plot_height=700, match_aspect=True)
plot_eyeclouds.xgrid.visible = False
plot_eyeclouds.ygrid.visible = False
plot_eyeclouds.xaxis.visible = False
plot_eyeclouds.xaxis.visible = False
plot_eyeclouds.image_rgba(image='thumbnails', x='MappedFixationPointX', y='MappedFixationPointY', dw='FixationDuration', dh='FixationDuration', source=ds) #trying to draw the points






show(plot_eyeclouds)
