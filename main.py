import joblib
from flask import Flask, jsonify, request
import pandas as pd
from sklearn import datasets

app = Flask(__name__)


@app.route("/", methods = ['GET'])
def test():
    return jsonify({'message' : "Hello!"})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
