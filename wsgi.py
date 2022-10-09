import uuid
import requests
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from markupsafe import escape
from pymongo import MongoClient

application = Flask(__name__, instance_relative_config=True)
# flask config: https://flask.palletsprojects.com/en/2.2.x/config/
application.config['TESTING'] = True

# clean-up: https://pymongo.readthedocs.io/en/stable/examples/authentication.html
application.config["MONGO_URI"] = "mongodb://root:example@mongo:27017"
client = MongoClient(application.config["MONGO_URI"])


@application.route('/')
def index():
    return render_template("index.html")


@application.route('/data')
def pirate():
    return render_template("deutsch.json")


@application.route('/question1')
def question1():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("question1.html", data=data)


@application.route('/flexquestion')
def flexquestion():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("flexquestion.html", data=data)


@application.route('/formgrid', methods=['GET', 'POST'])
def formgrid():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        data = [
            {"Noun": "Laptop", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "Laptop"},
            {"Noun": "E-Mail", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "EMail"},
            {"Noun": "Handy", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "CellPhone"}
        ]
        return render_template("formgrid.html", data=data)


@application.route('/formgrid2', methods=['GET', 'POST'])
def formgrid2():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        data = [
            {"Noun": "Laptop", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "Laptop"},
            {"Noun": "E-Mail", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "EMail"},
            {"Noun": "Handy", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "CellPhone"}
        ]
        return render_template("formgrid2.html", data=data)


@application.route('/radiobutton')
def radiobutton():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("radiobutton.html", data=data)


# allow both GET and POST requests
@application.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                      <h1>The language value is: {}</h1>
                      <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
               <form method="POST">
                   <div><label>Language: <input type="text" name="language"></label></div>
                   <div><label>Framework: <input type="text" name="framework"></label></div>
                   <input type="submit" value="Submit">pi
               </form>'''


# GET requests will be blocked
@application.route('/json-echo', methods=['POST'])
def json_echo():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    return jsonify(data), 200


@application.route('/json-form', methods=['GET', 'POST'])
def json_form():
    if request.method == 'POST':
        data = request.form
        # return data # => returns identical JSON output
        return jsonify(data), 200

    else:
        return render_template("jsonform.html")


# flask> db.questions.find({},{_id:0,cif:1,quid:1,name:1})
@application.route('/mongo')
def mongo():
    db = client.flask
    # answer = db.list_collection_names()
    collection = db.quizzes
    answer = collection.find_one({}, {'_id': 0})
    # answer = collection.find_one({}, {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1})
    # answer = collection.find_one({'data': {'$elemMatch': {"Noun": "Bleistift"}}},
    #                              {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1})
    return jsonify(answer), 200


@application.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'


# @application.route('/questions/<uuid:quid>')
# def show_question_id(quid):
#     # returns 404 if uuid is invalid # https://www.geeksforgeeks.org/python-404-error-handling-in-flask/
#     # QID-05db84d8-27ac-4067-9daa-d743ff56929b
#     # i.e. questions/05db84d8-27ac-4067-9daa-d743ff56929b
#     _quid = escape(quid)
#     try:
#         uuid.UUID(str(_quid))
#         return f'Quid {_quid}'
#     except ValueError:
#         return f'Invalid {escape(quid)}'
#

@application.route('/questions/<quid>')
def show_question_id(quid):
    # any/uuid return 404 if uuid is invalid # https://www.geeksforgeeks.org/python-404-error-handling-in-flask/
    # QID-05db84d8-27ac-4067-9daa-d743ff56929b - questions/05db84d8-27ac-4067-9daa-d743ff56929b
    _quid = escape(quid)
    try:
        uuid.UUID(str(_quid))
        return f'Valid uuid{": " + _quid}'
    except ValueError:
        return f'Invalid uuid{escape(": " + quid)}'


@application.route('/api')
def runnable():
    r = requests.get('https://api.github.com/users/runnable')
    return jsonify(r.json())


@application.route('/isready')
def isready():
    return 'isReady'


@application.route('/isalive')
def isalive():
    return 'isAlive'


if __name__ == "__main__":
    application.run()
