import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory, g, render_template
import sqlite3
import secrets
from config import Config as Configvalues
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Configvalues.UPLOAD_FOLDER
DATABASE = Configvalues.DATABASE
random.seed()


@app.route('/')
def homepage():
    return render_template('home.html')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Configvalues.ALLOWED_EXTENSIONS


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload/<string:key>', methods=['GET', 'POST'])
def upload_file(key):
    # TODO: Refactor code
    if request.method == 'POST':
            # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            keylist = query_db("select * from key where allowed_keys = ?", (key,))
            if not keylist:
                return '''<h2>ERROR: </h2> <p>Your token is not authorized to use this service.</p>'''
            else:
                extension = file.filename.split(".",1)[1]
                randnum = random.getrandbits(20)
                filename = str(randnum) + "." + extension
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))
    else:
        return render_template('upload.html')


@app.route('/keygen')
def keygen():
    key = secrets.token_hex(32)
    return key + '''<p>Send this key to ''' + Configvalues.OWNER + ''' to activate your account.'''


@app.route('/addaccount/<string:ownerkey>/<string:keytoadd>')
def addaccount(ownerkey, keytoadd):
    if ownerkey == Configvalues.OWNERKEY:
        try:
            query_db("INSERT INTO key (allowed_keys) VALUES (" + keytoadd + ");")
            db = getattr(g, '_database', None)
            db.commit()
            return '''<p>Done.</p>'''
        except sqlite3.IntegrityError:
            return '''This Key Already exists.'''
    else:
        return '''<p>LOL You are not the owner nice try!</p>'''


@app.route('/upload')
def uploadnokey():
    return'''You need to supply your key to do this! Simply add it to the end of /upload/ for it to work!'''


if __name__ == '__main__':
    app.run()
