from flask import Flask
from flaks_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///data/library'
                                         '.sqlite')

db.init_app(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
