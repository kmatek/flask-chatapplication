from flask import Blueprint
from flask import render_template, redirect, session, request, url_for, flash

view = Blueprint("views", __name__)


@view.route("/login", methods=('POST', 'GET'))
def login():
    """Enable to login to the chat room, and save name in session."""
    if 'name' in session:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        name = request.form["inputName"]
        if len(name) >= 3:
            session['name'] = name
            return redirect(url_for('views.home'))
        else:
            flash("Name must be longer than 1 character.")
    return render_template('login.html')


@view.route("/logout")
def logout():
    session.pop('name', None)
    return redirect(url_for("views.home"))


@view.route("/")
def home():
    """Chat view"""
    if 'name' not in session:
        return redirect(url_for('views.login'))
    return render_template('chat.html')
