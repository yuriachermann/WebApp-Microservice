from dataclasses import dataclass

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@db/db_microservice'
CORS(app)

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)


@dataclass
class Tool(db.Model):
    id: int
    title: str
    tool_num: str
    raw_image: str
    processed_image: str
    wear_area: float
    wear_length: float
    vb_max: float
    vb_mean: float

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    tool_num = db.Column(db.String(200))
    raw_image = db.Column(db.String(200))
    processed_image = db.Column(db.String(200))
    wear_area = db.Column(db.Float)
    wear_length = db.Column(db.Float)
    vb_max = db.Column(db.Float)
    vb_mean = db.Column(db.Float)

    def __init__(self, title, tool_num, raw_image, processed_image, wear_area, wear_length, vb_max, vb_mean):
        self.title = title
        self.tool_num = tool_num
        self.raw_image = raw_image
        self.processed_image = processed_image
        self.wear_area = wear_area
        self.wear_length = wear_length
        self.vb_max = vb_max
        self.vb_mean = vb_mean

    def __repr__(self):
        return '<Tool %r>' % self.title


@dataclass
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    date = db.Column(db.DateTime)

    UniqueConstraint('username', name='unique_username')

    def __init__(self, username, password, email, date):
        self.username = username
        self.password = password
        self.email = email
        self.date = date

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
