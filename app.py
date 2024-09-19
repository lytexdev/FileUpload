from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session, Response
from models import db, User, File
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

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


@app.before_request
def require_login():
    if 'user_id' not in session and request.endpoint not in ['login', 'download', 'static']:
        return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('upload'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                return redirect(url_for('upload'))
            else:
                flash('Invalid credentials', 'error')

    except SQLAlchemyError as e:
        flash('An error occurred while trying to log in.', 'error')
        app.logger.error(f"Login error: {str(e)}")

    return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            file = request.files['file']
            password = request.form['password']
            info = request.form['info']

            if file and password:
                filename = secure_filename(file.filename)

                existing_file = File.query.filter_by(filename=filename).first()
                if existing_file:
                    flash('File already exists!', 'error')
                    return redirect(url_for('upload'))

                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                new_file = File(filename=filename, info=info)
                new_file.set_password(password)
                db.session.add(new_file)
                db.session.commit()

                flash('File uploaded successfully!', 'success')
                return redirect(url_for('upload'))

    except IntegrityError:
        db.session.rollback()
        flash('A file with that name already exists.', 'error')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while uploading the file.', 'error')
        app.logger.error(f"Upload error: {str(e)}")
    except Exception as e:
        flash('An unexpected error occurred.', 'error')
        app.logger.error(f"General error: {str(e)}")

    return render_template('upload.html')


@app.route('/file/<filename>', methods=['GET', 'POST'])
def download(filename):
    try:
        file_entry = File.query.filter_by(filename=filename).first()

        if not file_entry:
            flash('File not found!', 'error')
            return redirect(url_for('upload'))

        if request.method == 'POST':
            password = request.form['password']

            if file_entry.check_password(password):
                return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
            else:
                flash('Incorrect password!', 'error')

    except SQLAlchemyError as e:
        flash('An error occurred while trying to access the file.', 'error')
        app.logger.error(f"Download error: {str(e)}")
    except Exception as e:
        flash('An unexpected error occurred.', 'error')
        app.logger.error(f"General error: {str(e)}")

    return render_template('download.html', filename=filename, info=file_entry.info)


@app.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        flash('You have been logged out.', 'success')
    except Exception as e:
        flash('An error occurred while logging out.', 'error')
        app.logger.error(f"Logout error: {str(e)}")

    return redirect(url_for('login'))


@app.route('/robots.txt')
def robots_txt():
    try:
        if app.config['SEARCH_ENGINE_INDEXING']:
            response = Response("User-agent: *\nDisallow: /", mimetype="text/plain")
        else:
            response = Response("User-agent: *\nAllow: /", mimetype="text/plain")
        return response
    except Exception as e:
        app.logger.error(f"Error generating robots.txt: {str(e)}")
        return Response("Error generating robots.txt", status=500)


if __name__ == '__main__':
    try:
        with app.app_context():
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            db.create_all()
        app.run(debug=os.getenv('DEBUG'), host='0.0.0.0', port=os.getenv('PORT'))
    except Exception as e:
        app.logger.error(f"App startup error: {str(e)}")
