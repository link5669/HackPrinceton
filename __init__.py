from operator import methodcaller
from flask import session
from flask import request, render_template, Flask, redirect, url_for
from midiutil.MidiFile3 import MIDIFile
from os import urandom
import pymongo
from music_logic.main import start

client = pymongo.MongoClient("mongodb+srv://link5669:princeton@cluster0.uayhxkd.mongodb.net/?retryWrites=true&w=majority")
db = client.test

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

def image_to_midi():
    start("music_logic/resources/samples/piano.png")
    return "BLANKS"

@app.route("/", methods=['GET'])
def welcome():
    '''
    Welcome Page
    '''
    return render_template("mainpage.html")


@app.route("/sheet/upload", methods=['GET', 'POST'])
def upload():
    '''
    Page for uploading sheet music
    '''
    return render_template("upload.html")


@app.route("/sheet/compiling", methods=['GET', 'POST'])
def compile():
    '''
    In between for processing the music sheet uploaded
    '''

    #value processed represents if it was able to be compiled properly or not
    if request.method == "GET":
        return "Not here"
    elif request.method == "POST":
        #image_to_midi() is return of miles' end of the project
        print("post req activated!")
        print(request.form["image-upload"])
        midi = image_to_midi(request.form["image-upload"])
        session["midi"] = midi
        processed = midi != None
        if processed:
            return "worked"
            #return redirect("/sheet/processed")
        else:
            return "didnt worked"
            #return redirect("/sheet/failed")

@app.route("/sheet/processed", methods=['GET', 'POST'])
def process():
    '''
    Page for uploading sheet music
    '''
    return render_template("processed.html")


@app.route("/sheet/failed", methods=['GET', 'POST'])
def fail():
    '''
    Page for failed upload -> maybe replace with a failed prompt and redirect to upload?
    '''
    return render_template("failed.html")

@app.route('/login',methods = ['POST'])
def login():
   dblist = client.list_database_names()
   if "user_info" in dblist:
        print("The database exists.")
   else:
        mydb = client["user_info"]
        mycol = mydb["customers"]
        mydict = { "username": "init", "password": "init" }
   x = mycol.insert_one(mydict)
   if request.method == 'POST':
      user = request.form['user_name']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/login',methods = ['GET'])
def see_login():
    return render_template("signup.html")

def main():
    # image_to_midi()
    """
    false if this file imported as module
    debugging enabled
    """
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
