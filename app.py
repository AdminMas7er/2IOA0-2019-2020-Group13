import os
import app
import pandas as pd
import random
import numpy as np
import time
import cv2 as cv2
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt

from  flask import Flask, flash, render_template, request, redirect, url_for, request
from werkzeug.utils import secure_filename
from PIL import Image
from bokeh.plotting import figure, curdoc, show, output_file
from bokeh.palettes import turbo
from bokeh.embed import components
from bokeh.models import FuncTickFormatter, ColumnDataSource 

ALLOWED_EXTENSIONS = {'csv','jpg', 'jpeg'}

app=Flask(__name__,static_folder='uploads')
app.secret_key = "key"
#configuring the upload folder and the maximum size

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#defines the allowed file types

stimuli=""
stimuli_url=""
data_url=""

UPLOAD_FOLDER=os.path.join(app.root_path,'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST']) #http methods, GET is managing information not secure, POST is Secure
def csv_upload_file():

    if request.method== 'POST': #if the transfer is Secure
        #checks if the post has the file
        if 'file' not in request.files:
            flash('no file part') #if the file is not there, get an error
            return redirect (request.url)
        file =request.files['file']
        #if user does not select a file, an empty file is uploaded
        if file.filename== '':
            flash('no selected file')
            return redirect(request.url) 
            
        if file and allowed_file(file.filename):
                dataset=secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],dataset))
                
                return redirect(url_for('csv_file',dataset=dataset))

    return render_template("index.html")     

@app.route('/upload_csv/<dataset>',methods=['GET','POST'])
def csv_file(dataset): #file uploaded is a csv file, and image needs to be uploaded
    if request.method== 'POST': #if the transfer is Secure
        #checks if the post has the file
        if 'file' not in request.files:
            flash('no file part') #if the file is not there, get an error
            return redirect (request.url)
        file =request.files['file']
        #if user does not select a file, an empty file is uploaded
        if file.filename== '':
            flash('no selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            stimuli=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],stimuli))
            
            return redirect(url_for('graph_generate',stimuli=stimuli,dataset=dataset))    
    return render_template("upload_image.html")   

def data_received(stimuli,dataset):
    ip_address=request.remote_addr
    data_url = os.path.join(app.config['UPLOAD_FOLDER'],dataset)
    stimuli_path = os.path.join(app.config['UPLOAD_FOLDER'],stimuli)
    
    img_url='http://'+ip_address+':5000/uploads/'+stimuli+'/'
  
    return (ip_address,stimuli_path,img_url,data_url)

@app.route('/graph_generate/<dataset>/<stimuli>/')
def graph_generate(stimuli,dataset):
    
    ip_address,stimuli_path,img_url,data_url=data_received(stimuli,dataset)
    data=pd.read_csv(data_url,encoding = "latin1",delim_whitespace=True)

    stimuli_filter=data['StimuliName']==stimuli
    mapped=data[stimuli_filter]

    user_array=mapped['user'].unique()

    #start of gaze plot code
    palette = turbo(256)

    img =  Image.open(stimuli_path)
    width, height = img.size

    plot_gazeplot = figure(plot_width =800 , plot_height=700, x_range=(0,width), y_range=(height,0))
    plot_gazeplot.image_url(url=[img_url], x=0, y=0, h=height, w=width, alpha=1)

    j=0
    specific_color = []

    for user in user_array:
        specific_color.append(palette[random.randint(0,255)])
        mapped.loc[mapped['user'] == user, 'color'] = specific_color[j]
        j=j+1
        index = (np.where(user_array==user))[0][0]
        color = '#' + str(specific_color[index][1:])
        points=mapped[mapped['user']==user].sort_values(by='Timestamp')
        plot_gazeplot.line(points['MappedFixationPointX'], points['MappedFixationPointY'], line_width=2, alpha=0.65, color=color)
        plot_gazeplot.circle(points['MappedFixationPointX'], points['MappedFixationPointY'],size=(points['FixationDuration']/25), color=points['color'], alpha=0.85)

    script_gazeplot, div_gazeplot = components(plot_gazeplot,wrap_script=False)

    #start of heatmap code

    ds = data[data['StimuliName'] == stimuli].reset_index().copy()
    io = plt.imread(stimuli_path)
    i = io.copy().astype(np.uint8)  #cast numpy array to specific type: Unsigned integer (0 to 255)

    if i.ndim == 2: #number of dimensions of array
        i = cv2.cvtColor(i, cv2.COLOR_GRAY2RGBA) #color gray
    else:
        if i.ndim == 3:
            i = cv2.cvtColor(i, cv2.COLOR_RGB2RGBA) #color from RGB

    i = np.flipud(i) ##flips array in the up/down direction

    #check is the point is inside the bounds
    bounds = (ds['MappedFixationPointX']>width) | (ds['MappedFixationPointY']>height) \
             | (ds['MappedFixationPointX']<0) | (ds['MappedFixationPointY']<0)

    ds = ds[np.logical_not(bounds)].reset_index().copy()

    #create numpy arrays for fixation point x, fixation point y and fixation duration
    point_x = np.array([])
    point_y = np.array([])
    duration = np.array([])

    for index, row in ds.iterrows():
        point_x = np.append(point_x, np.array([row['MappedFixationPointX']]))
        point_y = np.append(point_y, np.array([row['MappedFixationPointY']]))
        duration = np.append(duration, np.array([row['FixationDuration']]))

    #create histogram H using numpy histogram 2d
    H, x_edges, y_edges = np.histogram2d(point_y, point_x, bins=200, weights=duration)
    H = filters.gaussian_filter(H, sigma=4)  #gaussian filter
    H = np.flipud(H)  #flips array in the up/down direction

    #map the heatmap
    plot_heatmap = figure(plot_width=900, plot_height=700, x_range=(0, width), y_range=(height, 0))
    plot_heatmap.image_url(url=[img_url], x=0, y=0, h=height, w=width, alpha=1)
    plot_heatmap.image(image=[H], x=0, y=height, dw=width, dh=height, palette="Turbo11", global_alpha=0.5)

    script_heatmap, div_heatmap = components(plot_heatmap, wrap_script=False)

    #start of gaze stripe code

    coordinates_pairs = mapped[['MappedFixationPointX', 'MappedFixationPointY']].itertuples(index=False, name=None)
    coordinates = list(coordinates_pairs) #converts points in dataframe to a list of tuples of coordinates such as (x1, y1), (x2, y2), ...

    psize = 100 #size in pixels of cropped image

    image1 = Image.open(stimuli_path)
    img1 = image1.convert('RGBA') #converts to RGBA image to use

    cropped_images = []

    for x, y in coordinates:
       box = (x - psize / 2, y - psize / 2, x + psize / 2, y + psize / 2) #box is in format of (x1, y1, x2, y2) - x1y1 are top left and x2y2 are bottom right
       cropped_images.append(np.array(img1.crop(box)).view(np.uint32)[::-1])

    mapped['Image'] = cropped_images

    for user in user_array:
        mapped.loc[(mapped['user'] == user), 'Timestamp'] = np.arange((mapped['user'] == user).sum())

    user_row = dict(zip(user_array, range(user_array.shape[0]))) #stores row of each user where output should be printed, eg. - p1:0 -> output of user p1 is stored in row 0(row 1)
    mapped['UserRow'] = mapped['user'].replace(user_row)

    plot_gazestripe = figure(plot_width = 1500, plot_height=700, match_aspect=True)

    plot_gazestripe.xaxis.visible = False
    plot_gazestripe.xgrid.visible = False
    plot_gazestripe.ygrid.visible = False

    plot_gazestripe.yaxis.ticker = list(user_row.values())
    plot_gazestripe.yaxis.formatter = FuncTickFormatter(args=dict(user_coords={v: k for k, v in user_row.items()}), code="return user_coords[tick];") #names each tick according to user

    source = ColumnDataSource(mapped) #so that columns used for image, x and y can be recognized

    img_size = 1
    plot_gazestripe.image_rgba(image='Image', x='Timestamp', y='UserRow', dw=img_size, dh=img_size, source=source) #plots each image in gaze stripe

    script_gazestripe, div_gazestripe = components(plot_gazestripe,wrap_script=False)

    return render_template('layout.html',script_gazeplot=script_gazeplot,div_gazeplot=div_gazeplot, script_gazestripe=script_gazestripe,div_gazestripe=div_gazestripe, script_heatmap=script_heatmap,div_heatmap=div_heatmap)

if __name__=="__main__":
    app.run(debug=True)