#needs to be pasted and run in the same directory folder where your python is installed

import pandas as pd
import random
import numpy as np
from PIL import Image
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import turbo

data = pd.read_csv("/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace = True)

output_file('image.html')

stimuli = '02_Berlin_S1.jpg'
stimuli_url = '/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/stimuli/02_Berlin_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

user_array=mapped['user'].unique()

palette = turbo(256)

img =  Image.open(stimuli_url)
width, height = img.size

def gazeplot_show(): 
    
        output_file('image.html')

        p = figure(plot_width = 900, plot_height=700, x_range=(0,width), y_range=(height,0))

        p.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)

        j=0
        specific_color = []

        for user in user_array:
                specific_color.append(palette[random.randint(0,255)])
                mapped.loc[mapped['user'] == user, 'color'] = specific_color[j]
                j=j+1
                index = (np.where(user_array==user))[0][0]
                color = '#' + str(specific_color[index][1:])
                points=mapped[mapped['user']==user].sort_values(by='Timestamp')
                p.line(points['MappedFixationPointX'], points['MappedFixationPointY'], line_width=2, alpha=0.65, color=color)
                p.circle(points['MappedFixationPointX'], points['MappedFixationPointY'],size=(points['FixationDuration']/25), color=points['color'], alpha=0.85)
        
        show(p)  # open a browser

gazeplot_show()