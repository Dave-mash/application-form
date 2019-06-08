from flask import Flask
import os
import re
from flask import jsonify, make_response, request

from database import InitializeDb

app = Flask(__name__)

db = InitializeDb(os.getenv('FLASK_DATABASE_URI'))
db.create_tables()
db.connection.commit()

@app.route('/')
def get():
    """ This route displays all the users """

    users_list = []

    try:
        db.cursor.execute(
            "SELECT (name, email, phone) FROM test_users;"
        )
        return make_response(jsonify({
            "status": 200,
            "users": users_list
        }), 200)
    except:
        
        return make_response(jsonify({
            "status": 400,
            "error": "Bad request"
        }), 400)

@app.route('/insert', methods=['POST'])
def post():
    """ This route inserts a user """
    data = request.get_json()

    reg_email = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

    if not re.match(reg_email, str(data['email'])):
        return jsonify({
            "error": "Invalid email address!",
            "status": 422
        })
    if not data['name'].isalpha():
        return jsonify({
            "error": "Enter a valid name!",
            "status": 422
        })

    user = dict(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )

    keys = ", ".join(user.keys())
    values = tuple(user.values())


    try:
        db.cursor.execute(
            "INSERT INTO test_users ({}) VALUES {};".format(keys, values)
        )
        db.connection.commit()
        return make_response(jsonify({
            "status": 201,
            "message": "posted successfully"
        }), 201)
    except:
        
        return make_response(jsonify({
            "status": 400,
            "error": "Bad request"
        }), 400)



if __name__ == "__main__":
    app.run()