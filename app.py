import os
import app
from  flask import Flask,flash,render_template,request,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import matplotlib.image
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import imshow
import seaborn as sns

sns.set()
UPLOAD_FOLDER = './uploads' #MAKE SURE TO CREATE A FOLDER FOR THIS IN THE CODE FOLDER
ALLOWED_EXTENSIONS = {'csv','jpg', 'jpeg'}

app=Flask(__name__)
app.secret_key = "key"
#configuring the upload folder and the maximum size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#defines the allowed file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#uploader tool route
@app.route('/',methods=['GET','POST']) #http methods, GET is managing information not secure, POST is Secure
def upload_file():
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
        if file and allowed_file(file.filename): #if the file is a csv, it displays is and saves it in a folder
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                                   
    return render_template("index.html")                                    
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if filename.endswith('.csv'):
        global data
        data=pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'],filename),encoding = "latin1",delim_whitespace=True)
        return redirect('/')
    if filename.endswith('.jpg') or filename.endswith('.jpeg'):
        global img
        img=mpimg.imread(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        global stimuli
        stimuli=filename
        stimuli_filter=data['StimuliName']==stimuli
        mapped=data[stimuli_filter]
        user_array=mapped['user'].unique()
        fig,ax=plt.subplots(sharex=True,sharey=True,figsize=(25,25))
        def randomColor():
            cr=np.random.randint(0,255)
            cg=np.random.randint(0,255)
            cb=np.random.randint(0,255)
            color='#'+str(hex(cr)[2:].zfill(2)+hex(cg)[2:].zfill(2)+hex(cb)[2:].zfill(2)+'FF').upper()
            for user in user_array:
                points=mapped[mapped['user']==user].sort_values(by='Timestamp')
                rand =[randomColor() for point in points]
                randC = sns.set_palette(sns.color_palette(rand))
                sns.scatterplot(x='MappedFixationPointX',y='MappedFixationPointY',size='FixationDuration',sizes=(100,900),alpha=0.85,palette=randC,data=points,legend=False,ax=ax)
                sns.lineplot(x='MappedFixationPointX',y='MappedFixationPointY',palette=randC,data=points,ax=ax)
            for i,point in points.reset_index().iterrows():
                ax.text(x=point['MappedFixationPointX'], y=point['MappedFixationPointY'], s=i, horizontalalignment='center', color='black',size='medium', weight='semibold')
        fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'],'graph.png'))
    return render_template("display.html",name=filename,data=data)

if __name__=="__main__":
    app.run(debug=True)

