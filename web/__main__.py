from .service import app
import os

app.secret_key = 'hackathon2022'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = "data"

#TODO use dotfile
os.environ["UPLOAD_FOLDER"] = app.config['UPLOAD_FOLDER']

app.run(host='0.0.0.0', port=5000)