import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from routing.database import Database

auth = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@auth.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    db = Database().admin.get_db().cursor()
    username = session.get("Username")

    if username is None:
        g.user = None
    else:
        db.execute("SELECT * FROM User WHERE Username = %s", (username,))
        g.user = (db.fetchone())


@auth.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = Database().admin.get_db().cursor()

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO User VALUES (%s, %s)", (username, generate_password_hash(password))
                )
            except Exception as e:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html", error=error)


@auth.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = Database().admin.get_db().cursor()
        db.execute("SELECT * FROM User WHERE Username = %s", (username,))
        user = db.fetchone()
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["Password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["Username"] = user["Username"]
            return redirect(url_for("user_routes.retrieve_user_list"))
        flash(error)

    return render_template("auth/login.html", error=error)


@auth.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
