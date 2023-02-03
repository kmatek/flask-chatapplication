from flask import Blueprint
from flask import render_template, redirect, session, request, url_for, flash, jsonify, current_app # noqa

from .db import Database

view = Blueprint("views", __name__)

NAME_SESSION_KEY = 'name'


@view.route("/login", methods=('POST', 'GET'))
def login():
    """Enable to login to the chat room, and save name in session."""
    if NAME_SESSION_KEY in session:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        if current_app.config.get('TESTING', False):
            db = Database(test=True)
        else:
            db = Database()
        name = request.form["inputName"].lower()

        if len(name) >= 3:
            if db.save_name(name):
                session[NAME_SESSION_KEY] = name
                return redirect(url_for('views.home'))
            else:
                flash("Someone already is using this name.")
        else:
            flash("Name must be longer than 2 character.")
    return render_template('login.html')


@view.route("/logout")
def logout():
    name = session.pop(NAME_SESSION_KEY, None)
    # Remove name
    if current_app.config.get('TESTING', False):
        db = Database(test=True)
    else:
        db = Database()
    db.remove_name(name)
    db.close()
    return redirect(url_for("views.home"))


@view.route("/")
def home():
    """Chat view"""
    if NAME_SESSION_KEY not in session:
        return redirect(url_for('views.login'))
    return render_template('chat.html')


@view.route("/get-name")
def get_name() -> jsonify:
    """Get logged user's name"""
    data = {"name": ""}

    if NAME_SESSION_KEY in session:
        data['name'] = session[NAME_SESSION_KEY]
    return jsonify(data)


@view.route('/get-messages')
def get_messages() -> jsonify:
    """Get old messages"""
    if current_app.config.get('TESTING', False):
        db = Database(test=True)
    else:
        db = Database()

    messages = db.get_messages(limit=50)
    mapped_msg = map(
        lambda x: {
            'name': x[1],
            'message': x[2],
            'date': str(x[3])[:-3]
        }, messages)
    db.close()

    return jsonify(list(mapped_msg))
