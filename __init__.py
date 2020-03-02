import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_migrate import Migrate

# Will hash and rehash for passwords from database for encryption
from werkzeug.security import generate_password_hash

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db, User

    db.init_app(app)
    migrate = Migrate(app, db)

    # MVC (Model, View Controller) Framework
    # create the controller which handles the http request which
    # then updates the data based on the model and finally view will show how the display should show to the user

    # added a route 'sign_up', render_template is the view
    @app.route('/sign_up', methods=('GET', 'POST'))
    def sign_up():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required'
            elif not password:
                error = 'Password is required'
            # checks for an exisitng username executes a SQL select * from username where username=username
            elif User.query.filter_by(username=username).first():
                error = 'Username is already taken'

            # add user to database if there is no error
            if error is None:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                flash("Successfully signed up! Please log in.", 'success')
                return redirect(url_for('log_in'))

            flash(error,'error')

        return render_template('sign_up.html')

    @app.route('/log_in')
    def log_in():
        return "Login"

    return app