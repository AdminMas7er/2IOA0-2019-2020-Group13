import pandas as pd
import random
import numpy as np
from PIL import Image
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import RdYlGn11

data = pd.read_csv(r"C:/Users/20191071/Desktop/MetroMapsEyeTracking/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv",encoding = "latin1",delim_whitespace=True)

output_file('image.html', mode='inline')

stimuli = '01_Antwerpen_S1.jpg'
stimuli_url = '/Users/20191071/Desktop/MetroMapsEyeTracking/MetroMapsEyeTracking/stimuli/01_Antwerpen_S1.jpg'

stimuli_filter = data['StimuliName'] == stimuli
mapped = data[stimuli_filter]

user_array = mapped['user'].unique()

palette = RdYlGn11

img = Image.open(stimuli_url)
width, height = img.size

users = mapped['user'].count()


def heatmap_show():
    p = figure(plot_width=900, plot_height=700, x_range=(0, width), y_range=(height, 0))

    p.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)

    for user in user_array:
        points = mapped[mapped['user'] == user].sort_values(by='Timestamp')
        p.hex(x=mapped['MappedFixationPointX'], y=mapped['MappedFixationPointY'], size=(points['FixationDuration'] / 25),
              fill_color=palette)

    show(p)

heatmap_show()