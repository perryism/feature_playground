from flask import Flask, flash, request, redirect, url_for
import os

app = Flask(__name__)

from entities import Source
from flask import render_template 
from .libs.source_uploader import SourceUploader 

@app.route('/')
def index():
    return render_template("root/index.tmpl.html", sources=Source.all()) 

@app.route("/source", methods=["GET", "POST"])
def source():
    #https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if SourceUploader.allow(file):
            filename = SourceUploader(os.environ["UPLOAD_FOLDER"]).save(request.form["name"], file)
            #filename = SourceUploader(app.config['UPLOAD_FOLDER']).save(file)
            return redirect("/")
    else:
        return render_template("source/index.tmpl.html")