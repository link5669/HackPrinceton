from operator import methodcaller
from flask import session
from flask import request, render_template, Flask, redirect, url_for, make_response
from midiutil.MidiFile3 import MIDIFile
from os import urandom
import pymongo
from music_logic.main import start
from pymongo.errors import ConnectionFailure

client = pymongo.MongoClient("mongodb+srv://princeton:princeton@cluster0.uayhxkd.mongodb.net/?retryWrites=true&w=majority")
db = client.test
try:
    client.admin.command('ping')
except ConnectionFailure:
    print("Server not available")

app = Flask(__name__)
debug = True
app.secret_key = urandom(24)

def get_file_names():
    mydb = client["user_files"]
    collection = mydb["files"]
    item_details = collection.find()
    ret = []
    for item in item_details:
        if (item["username"] == request.cookies.get('username')):
            ret.append(item["file"])
    return ret

def image_to_midi(file_in,file_out):
    try:
        start("static/images/" + file_in.filename ,file_out)
        return 1
    except:
        return 0

@app.route("/", methods=['GET', 'POST'])
def upload():
    '''
    Page for uploading sheet music
    '''
    umess = ""
    print(request.cookies.get('username'))
    if (type(request.cookies.get('username')) is type(None) or str(request.cookies.get('username')) == "None"):
        return redirect("/login")
    else:
        umess = "Welcome, " + request.cookies.get('username')
    if request.method == "POST":
        file = request.files['image-upload']
        new_name = "/midi/" + file.filename[:file.filename.find(".")] + ".mid"
        processed = image_to_midi(file, "static/" + new_name) #function doesn't need to return midi -> can save within the static folder with filename
        if processed == 1:
            # send post request to sheet/processed where it plays the midi file and provides it for download -> deletes from static automatically?
            session["current_file"] = new_name
            return redirect(url_for('.process', midi_file=new_name, username=request.cookies.get('username')))
        elif processed == 0:
            # redirect request to sheet/upload about it not working
            return render_template("mainpage.html", login_message=umess, message="There's an issue with the image you uploaded. Try retaking or cropping the picture.")
    return render_template("mainpage.html", login_message=umess)        

@app.route("/processed", methods=['GET', 'POST'])
def process():
    '''
    Page for uploading sheet music
    '''
    midi_file = request.args['midi_file']
    if request.method == "POST":
        mydb = client["user_files"]
        mycol = mydb["files"]
        mydict = { "username": request.cookies.get('username'), "file": midi_file }
        x = mycol.insert_one(mydict)
        get_file_names()
        return redirect("/userdashboard")
    return render_template("processed.html", file_dir=midi_file)

@app.route("/failed", methods=['GET', 'POST'])
def fail():
    '''
    Page for failed upload -> maybe replace with a failed prompt and redirect to upload?
    '''
    return render_template("failed.html")

@app.route('/register',methods = ['POST'])
def register():
    dblist = client.list_database_names()
    mydb = client["user_info"]
    mycol = mydb["customers"]
    mydict = { "username": request.form['email'], "password": request.form['password'] }
    x = mycol.insert_one(mydict)
    make_response().set_cookie('username', request.form['email'])
    return render_template("mainpage.html", login_message="Welcome, " + request.form['email'])

@app.route('/register',methods = ['GET'])
def see_register():
   return render_template("signup.html")

@app.route('/login',methods = ['POST'])
def login():
    mydb = client["user_info"]
    collection = mydb["customers"]
    item_details = collection.find()
    print('dasljk')
    for item in item_details:
        if (item["username"] == request.form['email'] and
            item["password"] == request.form['password']):
            resp = make_response(render_template("mainpage.html", login_message="Welcome, " + request.form['email']))
            print('hello')
            resp.set_cookie('username', request.form['email'])
            session["username"] = request.form['email']
            return resp
    return render_template("login.html")

@app.route('/login',methods = ['GET'])
def see_login():
    print("alksjdlkasjd")
    return render_template("login.html")

@app.route('/userdashboard',methods = ['GET'])
def dashboard():
    if (type(request.cookies.get('username')) is not type(None)):
        track_list = get_file_names()
        print(track_list)
        return render_template("userdashboard.html", username=request.cookies.get('username'), track_list=track_list)
    else:
        return redirect("/")


def main():
    """
    false if this file imported as module
    debugging enabled
    """
    app.config['UPLOAD_FOLDER'] = "/temp"
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
