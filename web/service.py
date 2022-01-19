from flask import Flask, flash, request, redirect, url_for
import os

static_folder = os.environ.get("STATIC_FOLDER", "/static")
app = Flask(__name__)#, static_url_path='', static_folder=static_folder)

from entities import Source
from flask import render_template 
from .libs.csv_uploader import CsvUploader 
from web.decorators import decorate_source

@app.route('/')
def index():
    return render_template("root/index.tmpl.html", sources=[ decorate_source(s) for s in Source.all()] ) 

@app.route("/source/new", methods=["GET", "POST"])
def upload():
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

        if CsvUploader.allow(file):
            filename = CsvUploader(os.environ["UPLOAD_FOLDER"]).save(request.form["name"], file)
            #filename = SourceUploader(app.config['UPLOAD_FOLDER']).save(file)
            return redirect("/")
    else:
        return render_template("source/index.tmpl.html")

@app.route("/source/<int:source_id>", methods=["GET", "POST"])
def source(source_id):
    source = Source.find_by_id(source_id)
    return render_template("source/view.tmpl.html", source=source) 