import pandas as pd
import random
from PIL import Image
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.palettes import turbo

data = pd.read_csv("/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace = True)

output_file('image.html')

stimuli = '02_Berlin_S1.jpg'
stimuli_url = '/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/stimuli/02_Berlin_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

user_array=mapped['user'].unique()

palette = turbo(256)

specific_color = []

for user in user_array:
    specific_color.append(palette[random.randint(0,255)])

mapped['color']=""

j=0
for i in user_array:
   mapped.loc[mapped['user'] == i, 'color'] = specific_color[j]
   j=j+1

img =  Image.open(stimuli_url)
width, height = img.size

def bokeh_imshow(): 
    
        output_file('image.html')

        p = figure(plot_width = 900, plot_height=700, x_range=(0,width), y_range=(height,0))

        p.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)

        for user in user_array:
                points=mapped[mapped['user']==user].sort_values(by='Timestamp')
                p.line(points['MappedFixationPointX'], points['MappedFixationPointY'], line_width=2, alpha=0.65, color="black")
                p.circle(points['MappedFixationPointX'], points['MappedFixationPointY'],size=(points['FixationDuration']/25), color=points['color'], alpha=0.85)
        
        show(p)  # open a browser

bokeh_imshow()