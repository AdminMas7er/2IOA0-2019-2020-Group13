import os
from  flask import Flask,flash,render_template,request,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}




app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method== 'POST':
        #checks if the post has the file part
        if 'file' not in request.files:
            flash('no file part')
            return redirect (request.url)
        file =request.files['file']
        #if user does not select a file, browser also
        # submit an empty part with no filename
        if file.filename== '':
            flash('no selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('uploaded_file',
                                      filename=filename))                          
    return render_template("index.html")                                    
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data=pd.read_csv(filename,encoding = "cp1252")
    return render_template("table.html",name=filename,data=data)
if __name__=="__main__":
    app.run(debug=True)


