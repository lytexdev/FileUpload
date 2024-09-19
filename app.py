from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from models import db, User, File
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=os.getenv('DEBUG'), host='0.0.0.0', port=os.getenv('PORT'))
