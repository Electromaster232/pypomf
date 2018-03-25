import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory, g, render_template
import sqlite3
import secrets
from config import Config as Configvalues
import random
import time

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
                sqlname = filename.split(".",1)[0]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                values = (key, str(time.time()), sqlname, extension)
                query_db("INSERT INTO uploads (token, datetime, filename, fileext) VALUES (?, ?, ?, ?);", values)
                db = getattr(g, '_database', None)
                db.commit()
                if "/panel/" in request.referrer:
                    return redirect(request.referrer)
                else:
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
            query_db("INSERT INTO key (allowed_keys) VALUES (\"" + keytoadd + "\");")
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


@app.route('/panel/<string:token>')
def userpanel(token):
    keylist = query_db("select * from key where allowed_keys = ?", (token,))
    if not keylist:
        return '''<h2>Invalid Token</h2>'''
    else:
        filetotal = len(query_db("SELECT * from uploads"))
        files = query_db("SELECT * from uploads WHERE token = ? ORDER BY id desc", (token,))
        filelist = len(files)
        file1 = None
        file2 = None
        file3 = None
        file4 = None
        file5 = None
        try:
            file1 = str(files[0][3]) + "." + str(files[0][4])
            file2 = str(files[1][3]) + "." + str(files[1][4])
            file3 = str(files[2][3]) + "." + str(files[2][4])
            file4 = str(files[3][3]) + "." + str(files[3][4])
            file5 = str(files[4][3]) + "." + str(files[3][4])
        except IndexError:
            pass
        return render_template("panel.html", filenum=filelist, url="/../upload/" + token, file1=file1,
                               file2=file2, file3=file3, file4=file4,
                               file5=file5, totalfiles=filetotal)


@app.route('/panel', methods=['GET', 'POST'])
def panel():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        url = "/panel/" + request.form['token']
        return redirect(url)


# Hack to fix users clicking on non-existant img links
@app.route('/None')
def none():
    if request.referrer == None:
        return redirect("/../")
    else:
        return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True)
