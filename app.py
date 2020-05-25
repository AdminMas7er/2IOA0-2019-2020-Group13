import os
import app
from  flask import Flask,flash,render_template,request,redirect,url_for,send_from_directory,session
from werkzeug.utils import secure_filename
import pandas as pd
import random
import numpy as np
from PIL import Image
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import turbo
from bokeh.embed import components

UPLOAD_FOLDER = './uploads' #MAKE SURE TO CREATE A FOLDER FOR THIS IN THE CODE FOLDER
ALLOWED_EXTENSIONS = {'csv','jpg', 'jpeg'}

app=Flask(__name__)
app.secret_key = "key"
#configuring the upload folder and the maximum size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#defines the allowed file types

stimuli=""
stimuli_url=""
data_url=""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST']) #http methods, GET is managing information not secure, POST is Secure
def initial_upload_file():

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
                data_url = os.path.join(app.config['UPLOAD_FOLDER'],dataset)
                return redirect(url_for('csv_file',data_url=data_url))

    return render_template("index.html")     

@app.route('/uploads/<data_url>',methods=['GET','POST'])
def csv_file(data_url): #file uploaded is a csv file, and image needs to be uploaded
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
            
            return redirect(url_for('gazeplot_generate',stimuli=stimuli,data_url=data_url))    
    return render_template("upload_image.html")   

@app.route('/image_generate/<data_url>/<stimuli>/')
def gazeplot_generate(stimuli,data_url):
    stimuli_url = os.path.join(app.config['UPLOAD_FOLDER'],stimuli)
    data=pd.read_csv(data_url,encoding = "latin1",delim_whitespace=True)
    stimuli_filter=data['StimuliName']==stimuli
    mapped=data[stimuli_filter]

    user_array=mapped['user'].unique()

    palette = turbo(256)

    img =  Image.open(stimuli_url)
    width, height = img.size

    directory = os.path.dirname(os.path.realpath(__file__))[2:]
    newPath = directory.replace(os.sep, '/') + '/' + stimuli

    plot = figure(plot_width =800 , plot_height=700, x_range=(0,width), y_range=(0,height))
    plot.image_url(url=[newPath], x=0, y=0, h=height, w=width, alpha=1)

    j=0
    specific_color = []

    for user in user_array:
        specific_color.append(palette[random.randint(0,255)])
        mapped.loc[mapped['user'] == user, 'color'] = specific_color[j]
        j=j+1
        index = (np.where(user_array==user))[0][0]
        color = '#' + str(specific_color[index][1:])
        points=mapped[mapped['user']==user].sort_values(by='Timestamp')
        plot.line(points['MappedFixationPointX'], points['MappedFixationPointY'], line_width=2, alpha=0.65, color=color)
        plot.circle(points['MappedFixationPointX'], points['MappedFixationPointY'],size=(points['FixationDuration']/25), color=points['color'], alpha=0.85)

    script, div = components(plot,wrap_script=False)
    return render_template('layout.html', plot_script=script, plot_div=div)
if __name__=="__main__":
    app.run(debug=True)