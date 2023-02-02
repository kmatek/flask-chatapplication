from flask import Blueprint
from flask import render_template, redirect, session, request, url_for, flash, jsonify # noqa

view = Blueprint("views", __name__)

NAME_SESSION_KEY = 'name'


@view.route("/login", methods=('POST', 'GET'))
def login():
    """Enable to login to the chat room, and save name in session."""
    if NAME_SESSION_KEY in session:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        name = request.form["inputName"]
        if len(name) >= 3:
            session[NAME_SESSION_KEY] = name
            return redirect(url_for('views.home'))
        else:
            flash("Name must be longer than 2 character.")
    return render_template('login.html')


@view.route("/logout")
def logout():
    session.pop(NAME_SESSION_KEY, None)
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
