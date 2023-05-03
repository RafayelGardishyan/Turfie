from .db.models import User, Group, Turf
from flask import Blueprint, redirect, render_template, request, url_for
from tortoise.exceptions import DoesNotExist
import json
from . import validators

turfie = Blueprint("turfie", __name__)

config = json.load(open("config.json", "r"))

@turfie.route("/")
def index():
    return render_template("index.html")

@turfie.route("/register", methods=["GET", "POST"])
async def register():
    # Check if there is a post request with the username and password
    # If there is, create a new user with the username and password
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Validate the username and password
        if not validators.validate_username(username):
            return render_template("register.html", error=config["username"]["register_error_message"])
        if not validators.validate_username(password):
            return render_template("register.html", error=config["password"]["register_error_message"])

        # Check if the user already exists
        if await User.filter(username=username).count() > 0:
            return render_template("register.html", error="User already exists")
        
        # If the user doesn't exist, create the user
        user = await User.create(username=username, password=password)
        return redirect(url_for("turfie.login"))

    # If there isn't, return the register page
    return render_template("register.html")

@turfie.route("/login", methods=["GET", "POST"])
async def login():
    # Check if there is a post request with the username and password
    # If there is, check if the username and password are correct
    # If they are, log the user in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = await User.get(username=username)
        except DoesNotExist:
            return render_template("login.html", error="User does not exist")

        if user.check_password(password):
            return redirect(url_for("turfie.dashboard"))
        
        return render_template("login.html", error="Incorrect password")
        

    # If there isn't, return the login page
    return render_template("login.html")

