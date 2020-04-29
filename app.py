import os
from  flask import Flask,flash,render_template,request,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = './uploads' #MAKE SURE TO CREATE A FOLDER FOR THIS IN THE CODE FOLDER
ALLOWED_EXTENSIONS = {'csv'}




app=Flask(__name__)
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
            return redirect(url_for('uploaded_file',
                                      filename=filename))                          
    return render_template("index.html")                                    
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data=pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'],filename),encoding = "latin1",delim_whitespace=True)
    return render_template("table.html",name=filename,data=data)
if __name__=="__main__":
    app.run(debug=True)


