# this models class's purpose is to serve as an ORM (Object-Relational Mapper) using SQLAlchemy and converts our database items into an object this will allow us to manipulate and populate those items in the database
# We will also be using Flask-Migrate which will help with the database migration and changing database schema
# pipenv install psycopg2-binary Flask-SQLAlchemy Flask-Migrate for dependencies
# psycopg2 is a package to install to talk to sql
# database instance
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#DB connection and will be used to update model
    # db.Column map from database to instance will create an id attribute from reading of column
    # setups schema, with various columns expected in database
    # read and write will assign instances to this object
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    # will reference the author in the Note class, set lazy to true so that que doesn't update till search for note is initiated
    notes = db.relationship('Note', backref='author', lazy=True)

class Note(db.Model):
    # Creates a note object from database and purpose of note is to connect to the user by using foreign key
    # user to have many notes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
