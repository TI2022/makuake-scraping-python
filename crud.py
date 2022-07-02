from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": "hello",
    "susan": "bye"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


languages = [{'name': 'java'}, {'name': 'php'}, {'name': 'ruby'}]


@app.route("/", methods=['GET'])
@auth.login_required
def test():
    return jsonify({'message': "Hello, %s!" % auth.username()})


@app.route("/lang", methods=['GET'])
@auth.login_required
def returnAll():
    return jsonify({'langages': languages})


@app.route("/lang/<string:name>", methods=['GET'])
@auth.login_required
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'langages': langs[0]})


@app.route("/lang", methods=['POST'])
@auth.login_required
def addOne():
    language = {'name': request.json['name']}
    languages.append(language)
    return jsonify({'langages': languages})


@app.route("/lang/<string:name>", methods=['PUT'])
@auth.login_required
def editOne(name):
    langs = [language for language in languages if language['name'] == name]
    langs[0]['name'] = request.json['name']
    return jsonify({'langages': langs[0]})


@app.route("/lang/<string:name>", methods=['DELETE'])
@auth.login_required
def removeOne(name):
    langs = [language for language in languages if language['name'] == name]
    languages.remove(langs[0])
    return jsonify({'langages': languages})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
