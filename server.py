from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def homepage():
    return "<!doctype html><html>Hi! This is the home page.</html>"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
