# Eye Clouds Visualization

# Importing standard Python Libraries
import numpy as np
import pandas as pd
import random

# Importing specific modules
from PIL import Image, ImageDraw
from bokeh.models import ColumnDataSource, LassoSelectTool, UndoTool, RedoTool, HoverTool, ZoomInTool, ZoomOutTool
from bokeh.palettes import turbo
from bokeh.plotting import figure, output_file, show
from sklearn.cluster import KMeans

output_file("image.html", mode='inline')

data = pd.read_csv('C:/Users/20184080/Downloads/MetroMapsEyeTracking/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace = True)

stimuli = '01_Antwerpen_S1.jpg'
stimuli_url = 'C:/Users/20184080/Downloads/MetroMapsEyeTracking/MetroMapsEyeTracking/stimuli/01_Antwerpen_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

img =  Image.open(stimuli_url) 
img_rgb = img.convert('RGB') #converting the image in RGB values

Cluster_map=mapped[['MappedFixationPointX','MappedFixationPointY','FixationDuration']].copy() #creating a separate dataframe for the clustering

km=KMeans(n_clusters=7) #number of clusters
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

centers['FixationDuration']=centers['FixationDuration']/6.25 #resizing each image

# Sorting the dataset based from high Fixation Duration to low Fixation Duration
sorted_centers_raw = centers.sort_values(by = 'FixationDuration', ascending = False)
sorted_centers = sorted_centers_raw.reset_index()

# Determining diameter of each circle
circle_1d = sorted_centers['FixationDuration'][0]
circle_2d = sorted_centers['FixationDuration'][1]
circle_3d = sorted_centers['FixationDuration'][2]
circle_4d = sorted_centers['FixationDuration'][3]
circle_5d = sorted_centers['FixationDuration'][4]
circle_6d = sorted_centers['FixationDuration'][5]
circle_7d = sorted_centers['FixationDuration'][6]

# Saving X and Y coordinates for Hovertool under new names
sorted_centers['OriginalMappedFixationPointX'] = sorted_centers['MappedFixationPointX']
sorted_centers['OriginalMappedFixationPointY'] = sorted_centers['MappedFixationPointY']

# Reassigning values X and Y coordinates for reformation of the circles
sorted_centers['MappedFixationPointX'][0] = 500
sorted_centers['MappedFixationPointY'][0] = 500
sorted_centers['MappedFixationPointX'][1] = 500 + (0.5 * circle_1d) - (0.5 * circle_2d)
sorted_centers['MappedFixationPointY'][1] = 500 + circle_1d
sorted_centers['MappedFixationPointX'][2] = 500 + ((14/15) * circle_1d)
sorted_centers['MappedFixationPointY'][2] = 500 + ((2/3) * circle_1d)
sorted_centers['MappedFixationPointX'][3] = 500 + ((14/15) * circle_1d)
sorted_centers['MappedFixationPointY'][3] = 500 + ((1/3) * circle_1d) - circle_4d
sorted_centers['MappedFixationPointX'][4] = 500 + (0.5 * circle_1d) - (0.5 * circle_5d)
sorted_centers['MappedFixationPointY'][4] = 500 - circle_5d
sorted_centers['MappedFixationPointX'][5] = 500 - ((1.5/10) * circle_1d)
sorted_centers['MappedFixationPointY'][5] = 500 + ((1/3) * circle_1d) - circle_6d
sorted_centers['MappedFixationPointX'][6] = 500 - ((1.5/10) * circle_1d)
sorted_centers['MappedFixationPointY'][6] = 500 + ((2/3) * circle_1d) 
print(sorted_centers)

# Maps names of columns to arrays
ds = ColumnDataSource(sorted_centers)

## Creating the Eye Clouds visualization 

# Creating the plot
plot_eyeclouds = figure(plot_width =1000 , plot_height=700, match_aspect=True)

# Adjusting the grid
plot_eyeclouds.xgrid.visible = False
plot_eyeclouds.ygrid.visible = False
plot_eyeclouds.xaxis.visible = False
plot_eyeclouds.xaxis.visible = False

# Adjusting the background
plot_eyeclouds.background_fill_color = 'turquoise'
plot_eyeclouds.background_fill_alpha = 0.2

# Adding Tools 
plot_eyeclouds.add_tools(LassoSelectTool())
plot_eyeclouds.add_tools(UndoTool())
plot_eyeclouds.add_tools(RedoTool())
plot_eyeclouds.add_tools(ZoomInTool())
plot_eyeclouds.add_tools(ZoomOutTool())
plot_eyeclouds.add_tools(HoverTool(tooltips=[('X-Coordinate of Fixation', '@OriginalMappedFixationPointX'), ('Y-Coordinate of Fixation', '@OriginalMappedFixationPointY'), ('Total Duration of Fixation', '@FixationDuration')]))

# Creating RGB images inside the plot
plot_eyeclouds.image_rgba(image='thumbnails', x='MappedFixationPointX', y='MappedFixationPointY', dw='FixationDuration', dh='FixationDuration', source=ds) #trying to draw the points

# Call the plot
show(plot_eyeclouds)