from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from models import db, User, File
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SEARCH_ENGINE_INDEXING'] = os.getenv('SEARCH_ENGINE_INDEXING', 'False').lower() in ['true', '1', 't']
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)


@app.before_request
def disable_indexing():
    if app.config['SEARCH_ENGINE_INDEXING']:
        @app.after_request
        def add_header(response):
            response.headers['X-Robots-Tag'] = 'noindex, nofollow'
            return response


@app.route('/')
def index():
    return redirect(url_for('upload'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        password = request.form['password']
        info = request.form['info']

        if file and password:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_file = File(filename=filename, info=info)
            new_file.set_password(password)
            db.session.add(new_file)
            db.session.commit()

            flash('File uploaded successfully!')
            return redirect(url_for('upload'))

    return render_template('upload.html')


@app.route('/file/<filename>', methods=['GET', 'POST'])
def download(filename):
    file_entry = File.query.filter_by(filename=filename).first()

    if not file_entry:
        return "File not found!", 404

    if request.method == 'POST':
        password = request.form['password']

        if file_entry.check_password(password):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        else:
            flash('Incorrect password!')

    return render_template('download.html', filename=filename, info=file_entry.info)


if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        db.create_all()
    app.run(debug=os.getenv('DEBUG'), host='0.0.0.0', port=os.getenv('PORT'))
