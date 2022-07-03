import joblib
from flask import Flask, jsonify, request
import pandas as pd
from sklearn import datasets

app = Flask(__name__)


@app.route('/predict/<string:clf_file>', methods=['POST'])
def predict(clf_file):
    clf = joblib.load("{}.pkl".format(clf_file))
    data = request.json
    query = pd.DataFrame(data)
    cols = joblib.load("{}_cols.pkl".format(clf_file))
    query = query[cols]
    prediction = clf.predict(query)
    return jsonify({'prediction': prediction.tolist()})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
