from flask import Flask
import os
import re
from flask import jsonify, make_response, request, render_template

from database import InitializeDb

app = Flask(__name__)

db = InitializeDb(os.getenv('FLASK_DATABASE_URI'))
db.create_tables()
db.connection.commit()

users = [
    {
        "name": "Harry",
        "email": "harry@home.com",
        "phone": "78801236",
        "home_address": "Jalan Air",
        "office_address": "Jalan Angas"
    },
    {
        "name": "Harry",
        "email": "harry@home.com",
        "phone": "78801236",
        "home_address": "Jalan Air",
        "office_address": "Jalan Angas"
    },
    {
        "name": "Harry",
        "email": "harry@home.com",
        "phone": "78801236",
        "home_address": "Jalan Air",
        "office_address": "Jalan Angas"
    }
]

@app.route('/')
def get():
    """ This route displays all the users """
    users_list = []

    try:
        def json_output():
            return db.fetch_all(
                "SELECT row_to_json(row(name, email, phone, home_address, office_address)) FROM test_users INNER JOIN test_address ON test_address.user_email = test_users.email;"
            )

        users = [
            
        ]

        print('--->', json_output())
        for user in json_output():
            user = {
                "name": user[0]['f1'],
                "email": user[0]['f2'],
                "phone": user[0]['f3'],
                "home_address": user[0]['f4'],
                "office_address": user[0]['f5']
            }
            users_list.append(user)
        return render_template('index.html', users=users_list)
    except:
        
        return make_response(jsonify({
            "status": 400,
            "error": "Bad request"
        }), 400)

@app.route('/insert', methods=['POST'])
def post():
    """ This route inserts a user """
    user_info = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "phone": request.form.get('phone')
    }

    address = {
        "home_address": request.form.get('home-address'),
        "office_address": request.form.get('office-address')
    }

    reg_email = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

    if not re.match(reg_email, str(user_info['email'])):
        return jsonify({
            "error": "Invalid email address!",
            "status": 422
        })
    if not user_info['name'].isalpha():
        return jsonify({
            "error": "Enter a valid name!",
            "status": 422
        })

    user = dict(
        name=user_info['name'],
        email=user_info['email'],
        phone=user_info['phone']
    )

    keys = ", ".join(user.keys())
    values = tuple(user.values())

    user_address = dict(
        home_address=address['home_address'],
        office_address=address['office_address'],
        user_email=user_info['email']
    )

    address_keys = ", ".join(user_address.keys())
    address_values = tuple(user_address.values())


    try:
        db.cursor.execute(
            "INSERT INTO test_users ({}) VALUES {};".format(keys, values)
        )
        print('===>', [address_keys], [address_values])
        db.cursor.execute(
            "INSERT INTO test_address ({}) VALUES {};".format(address_keys, address_values)
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