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

img =  Image.open(stimuli_url)
img_rgb = img.convert('RGB') #converting the image in RGB values
h,w=img.size
npImg=np.array(img_rgb) #getting the RGB values in an array

Cluster_map=mapped[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].copy() #creating a separate dataframe for the clustering

km=KMeans(n_clusters=3) #number of clusters
km.fit(Cluster_map)
centers=pd.DataFrame(km.cluster_centers_,columns=Cluster_map.columns) #generating the centre of each cluster
centers_coords=centers[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].itertuples(index=False,name=None)  #putting the x, y, size values of each centre in a tuple
centre_pairs=list(centers_coords) #getting those tuples in a list

cropped_thumbs=[]

for x,y,size in centre_pairs: #the problem lies HERE
    box=[0,0,size,size] #size of crop, some issues with this
    alpha=Image.new('L',img.size,0)
    draw=ImageDraw.Draw(alpha)
    draw.pieslice(box,,360,fill=255) #another method for the elipse
    npAlpha=np.array(alpha)
    npImg=np.dstack((npImg,npAlpha)) #stacking the alpha with RGB
    cropped_thumbs.append(np.array(npImg).view(np.uint32)[::-1]) #this doesn't work, need to put them in an array
centers['thumbnails']=cropped_thumbs
ds=ColumnDataSource(centers)
img_size=1
plot_gazeplot = figure(plot_width =1000 , plot_height=700, match_aspect=True)
plot_gazeplot.image_rgba(image='thumbnails', x='MappedFixationPointX', y='MappedFixationPointY', dw=img_size, dh=img_size, source=ds) #trying to draw the points



plot_gazeplot.xgrid.visible = False
plot_gazeplot.ygrid.visible = False


show(plot_gazeplot)
