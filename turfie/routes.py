from .db.models import User, Group, Turf
from .db.db import get_groups_by_user
from flask import Blueprint, redirect, render_template, request, url_for, make_response
from tortoise.exceptions import DoesNotExist
import json
from . import validators

turfie = Blueprint("turfie", __name__)

config = json.load(open("config.json", "r"))

async def check_if_logged_in():
    if request.cookies.get("username"):
        return await User.get(username=request.cookies.get("username"))
    return False
        

@turfie.route("/")
async def index():
    if await check_if_logged_in():
        return redirect(url_for("turfie.dashboard"))
    return render_template("index.html")

@turfie.route("/dashboard")
async def dashboard():
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))
    
    return render_template("dashboard.html", 
                           logged_in=user, 
                           groups=await get_groups_by_user(user))


@turfie.route("/register", methods=["GET", "POST"])
async def register():
    # Check if the user is already logged in
    if await check_if_logged_in():
        return redirect(url_for("turfie.dashboard"))
    
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
    # Check if the user is already logged in
    if await check_if_logged_in():
        return redirect(url_for("turfie.dashboard"))

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
            response = make_response(redirect(url_for("turfie.dashboard")))
            response.set_cookie("username", username)
            return response
        
        return render_template("login.html", error="Incorrect password")
        

    # If there isn't, return the login page
    return render_template("login.html")

@turfie.route("/logout")
async def logout():
    response = make_response(redirect(url_for("turfie.dashboard")))
    response.set_cookie("username", "", expires=0)
    return response

