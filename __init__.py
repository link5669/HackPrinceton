from flask import session
from flask import request, render_template, Flask, redirect
from os import urandom
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


@app.route("/", methods=['GET'])
def welcome():
    '''
    Welcome Page
    '''
    return render_template("main.html")


@app.route("/sheet/upload", methods=['GET', 'POST'])
def welcome():
    '''
    Page for uploading sheet music
    '''
    return render_template("upload.html")


@app.route("/sheet/compiling", methods=['GET', 'POST'])
def welcome():
    '''
    In between for processing the music sheet uploaded
    '''

    #value processed represents if it was able to be compiled properly or not
    processed = True
    if processed:
        return redirect("/sheet/processed")

@app.route("/sheet/processed", methods=['GET', 'POST'])
def welcome():
    '''
    Page for uploading sheet music
    '''
    return render_template("processed.html")

def main():
    """
    false if this file imported as module
    debugging enabled
    """
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
