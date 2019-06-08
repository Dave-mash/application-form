from flask import Flask
from database import InitializeDb
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

db = InitializeDb(os.getenv('FLASK_DATABASE_URI'))
db.init_db(os.getenv('FLASK_DATABASE_URI'))
db.create_tables()
db.connection.commit()

if __name__ == "__main__":
    app.run()