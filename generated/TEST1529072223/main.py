#!/usr/bin/python

from flask import Flask
from  imports F1,F2,F3,F4

app = Flask(__name__)


@app.route("/F1/")
def F1():
    return "F1"



@app.route("/F2/")
def F2():
    return "F2"



@app.route("/F3/")
def F3():
    return "F3"
    
@app.route("/F4/")
def F4():
    return "F4"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)