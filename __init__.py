from operator import methodcaller
from flask import session
from flask import request, render_template, Flask, redirect, url_for
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
#why do we need secret keys? For this project it is not really necessary but...
#https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key
#I believe in a real life environment we should store the key somewhere safe in case of server crash
app.secret_key = urandom(24)
#   Things to work on:
#   Implimentationationation
#   Adding error messages and try and fails

#helper method

def image_to_midi(file_in,file_out):
    try:
        start("music_logic/resources/samples/piano.png",file_out)
        return True
    except:
        return False

# @app.route("/", methods=['GET'])
# def welcome():
#     '''
#     Welcome Page
#     '''
#     return render_template("mainpage.html")


@app.route("/", methods=['GET', 'POST'])
def upload():
    '''
    Page for uploading sheet music
    '''
    if request.method == "POST":
        print("post req activated!")
        file = request.files['image-upload']
        new_name = "static/" + file.filename[:file.filename.find(".")] + ".mid"
        processed = image_to_midi(file, new_name) #function doesn't need to return midi -> can save within the static folder with filename
        if processed:
            # send post request to sheet/processed where it plays the midi file and provides it for download -> deletes from static automatically?
            session["current_file"] = new_name
            return redirect("/processed")
            # return redirect("/sheet/processed")
        else:
            # redirect request to sheet/upload about it not working
            # return redirect("/sheet/failed")
            return render_template("mainpage.html", message="There's an issue with the image you uploaded. Try retaking or cropping the picture.")
    
    return render_template("mainpage.html")        

@app.route("/processed", methods=['GET', 'POST'])
def process():
    '''
    Page for uploading sheet music
    '''
    return render_template("processed.html", file_dir="static/test.mid")

    #return render_template("processed.html",file_dir=session["current_file"])


@app.route("/failed", methods=['GET', 'POST'])
def fail():
    '''
    Page for failed upload -> maybe replace with a failed prompt and redirect to upload?
    '''
    return render_template("failed.html")

@app.route('/register',methods = ['POST'])
def register():
   print("a")
   dblist = client.list_database_names()
   if "user_info" in dblist:
        print("The database exists.")
        mydb = client["user_info"]
        mycol = mydb["customers"]
        mydict = { "username": request.form['email'], "password": request.form['password'] }
        x = mycol.insert_one(mydict)
   else:
        mydb = client["user_info"]
        mycol = mydb["customers"]
   return render_template("mainpage.html")

@app.route('/register',methods = ['GET'])
def see_register():
   return render_template("signup.html")

@app.route('/login',methods = ['POST'])
def login():
   mydb = client["user_info"]
   collection = mydb["customers"]
   print(request.form['email'], request.form['password'])
   item_details = collection.find()
   for item in item_details:
       print(item)
       if (item["username"] == request.form['email'] and
           item["password"] == request.form['password']):
           print('login')
   return render_template("mainpage.html")

@app.route('/login',methods = ['GET'])
def see_login():
   return render_template("login.html")

def main():
    # image_to_midi()
    """
    false if this file imported as module
    debugging enabled
    """
    app.config['UPLOAD_FOLDER'] = "/temp"
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
