import numpy as np
import pandas as pd
import random

from PIL import Image
from bokeh.palettes import turbo
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show

output_file("image.html", mode='inline')

data = pd.read_csv("/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace = True)

stimuli = '18_Ljubljana_S1.jpg'
stimuli_url = '/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/stimuli/18_Ljubljana_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

user_array=mapped['user'].unique()

palette = turbo(256)

img =  Image.open(stimuli_url)
width, height = img.size
    
plot = figure(plot_width = 900, plot_height=700, x_range=(0,width), y_range=(height,0))

plot.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)

j=0
specific_color = []

for user in user_array:
    specific_color.append(palette[random.randint(0,255)])
    mapped.loc[mapped['user'] == user, 'color'] = specific_color[j]
    j=j+1
    index = (np.where(user_array==user))[0][0]
    color = '#' + str(specific_color[index][1:])

    points=mapped[mapped['user']==user]

    x = points['MappedFixationPointX']
    y = points['MappedFixationPointY']
    alpha=[]
    for item in x:
        alpha.append(0.5) #initial thickness of dots
    
    source = ColumnDataSource(data=dict(x=x, y=y, alpha=alpha, size=(points['FixationDuration']/25), color=points['color']))

    callback = CustomJS(args=dict(source=source), code="""
    const data = source.data;
    const f = cb_obj.value
    var x = data['x']
    var y = data['y']
    var size = data['size']
    var color = data['color']
    const alpha = data['alpha']
    for (var i = 0; i < x.length; i++) {
            alpha[i] = f
      }
    source.change.emit();
    """)
    plot.circle(x='x', y='y',size='size', color='color', alpha='alpha', line_alpha=0, source=source)
    slider = Slider(start=0, end=1, value=0.5, step=.05, title="Alpha")
    slider.js_on_change('value', callback)

    plot.line(points['MappedFixationPointX'], points['MappedFixationPointY'], line_width=2, alpha=0.8, color=color)
    #points.loc[(points['user'] == user), 'Timestamp'] = np.arange((points['user'] == user).sum())
    #plot.text(points['MappedFixationPointX'], points['MappedFixationPointY'], text=points['Timestamp'], color="black", text_font_size="5pt")

layout = column(slider, plot)

show(layout)