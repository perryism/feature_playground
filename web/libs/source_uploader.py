from werkzeug.utils import secure_filename
from entities import Source
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in SourceUploader.ALLOWED_EXTENSIONS

class SourceUploader:
    ALLOWED_EXTENSIONS = {'csv'}
    @staticmethod
    def allow(file):
        return file and allowed_file(file.filename)

    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def save(self, name, file):
        filename = secure_filename(file.filename)
        location = os.path.join(self.upload_folder, filename)
        file.save(location) 
        Source.insert(name=name, location=location)
        return filename