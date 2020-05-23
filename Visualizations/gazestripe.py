import numpy as np
import pandas as pd
from PIL import Image

from bokeh.io import show
from bokeh.models import FixedTicker, FuncTickFormatter, ColumnDataSource
from bokeh.plotting import figure, show, output_file
from bokeh.transform import dodge

data = pd.read_csv("/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace = True)

output_file('image.html', mode="inline")

stimuli = '01_Antwerpen_S1.jpg'
stimuli_url = '/Users/20190864/OneDrive - TU Eindhoven/Yemoe/TUe/Year 1/Quartile 4/DBL + Webtech/MetroMapsEyeTracking/stimuli/01_Antwerpen_S1.jpg'

stimuli_filter=data['StimuliName']==stimuli
mapped=data[stimuli_filter]

user_array=mapped['user'].unique()

#img =  Image.open(stimuli_url)
#width, height = img.size

coordinates = list(mapped[['MappedFixationPointX', 'MappedFixationPointY']].itertuples(index=False, name=None))
psize = 100

img = Image.open(stimuli_url).convert('RGBA')
cropped_images = []

for x, y in coordinates:
    box = (x - psize / 2, y - psize / 2, x + psize / 2, y + psize / 2)
    cropped_images.append(np.array(img.crop(box)).view(np.uint32)[::-1])

mapped['Image'] = cropped_images

for u in user_array:
    udf = (mapped['user'] == u)
    mapped.loc[udf, 'Timestamp'] = np.arange(udf.sum())

user_coords = dict(zip(user_array, range(mapped.shape[0])))
mapped['UserCoord'] = mapped['user'].replace(user_coords)

p = figure(match_aspect=True)
for r in [p.xaxis, p.xgrid, p.ygrid]:
    r.visible = False

p.yaxis.ticker = FixedTicker(ticks=list(user_coords.values()))
p.yaxis.formatter = FuncTickFormatter(args=dict(rev_user_coords={v: k for k, v in user_coords.items()}), code="return rev_user_coords[tick];")

ds = ColumnDataSource(mapped)
img_size = 1
p.image_rgba(image='Image',
             x=dodge('Timestamp', -img_size / 2), y=dodge('UserCoord', -img_size / 2),
             dw=img_size, dh=img_size, source=ds)
#p.rect(x='TimeCoord', y='UserCoord', width=img_size, height=img_size, source=ds,
       #line_dash='dashed', fill_alpha=0)

show(p)

#p = figure(plot_width = 900, plot_height=700, x_range=(0,width), y_range=(height,0))

#p.image_url(url=[stimuli_url], x=0, y=0, h=height, w=width, alpha=1)
