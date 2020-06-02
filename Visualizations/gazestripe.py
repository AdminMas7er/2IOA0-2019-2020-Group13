import numpy as np
import pandas as pd
import time
from PIL import Image

from bokeh.io import show
from bokeh.models import FuncTickFormatter, ColumnDataSource, HoverTool
from bokeh.plotting import figure, show, output_file

#start = time.process_time()

data = pd.read_csv("/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace = True)

stimuli = '01_Antwerpen_S1.jpg'
stimuli_url = '/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/stimuli/01_Antwerpen_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

user_array=mapped['user'].unique()

def gazestripe_show():

    output_file('image.html', mode="inline")

    coordinates_pairs = mapped[['MappedFixationPointX', 'MappedFixationPointY']].itertuples(index=False, name=None)
    coordinates = list(coordinates_pairs) #converts points in dataframe to a list of tuples of coordinates such as (x1, y1), (x2, y2), ...

    psize = 100 #size in pixels of cropped image

    image = Image.open(stimuli_url)
    img = image.convert('RGBA') #converts to RGBA image to use

    cropped_images = []

    for x, y in coordinates:
       box = (x - psize / 2, y - psize / 2, x + psize / 2, y + psize / 2) #box is in format of (x1, y1, x2, y2) - x1y1 are top left and x2y2 are bottom right
       cropped_images.append(np.array(img.crop(box)).view(np.uint32)[::-1])

    mapped['Image'] = cropped_images

    userlist=[]

    for user in user_array:
        mapped.loc[(mapped['user'] == user), 'Timestamp'] = np.arange((mapped['user'] == user).sum())
        userlist.append(int(user[1:]))
    
    user_row = dict(zip(user_array, userlist)) #stores row of each user where output should be printed according to user index, eg. - p1:1, p23:23 -> output of user p1, p23 is stored in row 1, 23 respectively
    
    mapped['UserRow'] = mapped['user'].replace(user_row)

    plot = figure(plot_width = 1500, plot_height=700, match_aspect=True)

    plot.xaxis.visible = False
    plot.xgrid.visible = False
    plot.ygrid.visible = False

    plot.yaxis.ticker = list(user_row.values())
    plot.yaxis.formatter = FuncTickFormatter(args=dict(user_coords={v: k for k, v in user_row.items()}), code="return user_coords[tick];") #names each tick according to user

    ds = ColumnDataSource(mapped)

    img_size = 1
    plot.image_rgba(image='Image', x='Timestamp', y='UserRow', dw=img_size, dh=img_size, source=ds) #plots each image in gaze stripe

    tools = "pan, wheel_zoom, box_zoom, reset, save, hover"

    plot.add_tools(HoverTool(tooltips=[('user, path index', '@UserRow, @Timestamp')]))

    show(plot)

gazestripe_show()

#print("Time taken to process image of " + str(psize) + " pixels each is " + str(time.process_time() - start) + " seconds", flush=True)
