from .db.models import JoinRequest, Notification, User, Group, Turf
from flask import Blueprint, redirect, render_template, request, url_for, make_response
from tortoise.exceptions import DoesNotExist
import json
from . import validators

turfie = Blueprint("turfie", __name__)

config = json.load(open("config.json", "r"))

async def check_if_logged_in():
    if request.cookies.get("username"):
        return await User.filter(username=request.cookies.get("username")).first()
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
    
    groups = await Group.get_groups_by_user(user)

    for group in groups:
        group.mycount = await Turf.get_turf_count_by_user(group.id, user.id)

    return render_template("dashboard.html", 
                           logged_in=user, groups=groups,
                           error=request.args.get("error", None),
                           message=request.args.get("message", None))


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
        if not validators.validate_password(password):
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

@turfie.route("/group/<int:groupid>")
async def grouppage(groupid: int):
    user = await check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    group = await Group.get(id=groupid)
    gusers = await group.users.all()
    admin = await group.admin.get()
    admin = admin.id == user.id

    if user not in gusers:
        return redirect(url_for("turfie.dashboard", error="You are not in this group"))

    user_turf_counts = await Turf.get_user_turf_counts(groupid)
    turf_history = await Turf.get_turf_history(groupid)

    return render_template("groupdashboard.html", 
                           group=group, user_turf_counts=user_turf_counts, 
                           logged_in=user, turf_history=turf_history, admin=admin
                           )

@turfie.route("/turf/add", methods=["POST"])
async def add_turf():
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    if int(request.form["registered_by"]) != user.id:
        return redirect(url_for("turfie.dashboard", error="Something went wrong, try to log in again"))
    
    for_user = await User.get(id=request.form["for_user"])
    group = await Group.get(id=request.form["groupid"])
    reason = request.form["reason"]

    await Turf.create(registered_by=user, for_user=for_user, group=group, reason=reason)

    return redirect(url_for("turfie.grouppage", groupid=group.id))

@turfie.route("/creategroup", methods=["GET", "POST"])
async def creategroup():
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    if request.method == "POST":
        group_name = request.form["group_name"]

        if not validators.validate_group_name(group_name):
            return redirect(
                url_for("turfie.dashboard", error=config["group_name"]["register_error_message"]))

        group = await Group.create(name=group_name, admin=user)

        jr = await JoinRequest.create(user=user, group=group)
        await jr.approve()

        return redirect(url_for("turfie.grouppage", groupid=group.id))
    
    return redirect(url_for("turfie.dashboard"))

@turfie.route("/join/<int:groupid>/")
async def join(groupid: int):
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    group = await Group.get(id=groupid)
    gusers = await group.users.all()

    for guser in gusers:
        if guser.id == user.id:
            return redirect(url_for("turfie.grouppage", groupid=groupid)) 

    if await JoinRequest.filter(user=user, group=group).count() > 0:
        return redirect(url_for("turfie.dashboard", message="You have already sent a join request to this group"))

    await JoinRequest.create(user=user, group=group)

    return redirect(url_for("turfie.dashboard", message="Join request sent"))

@turfie.route("/notifications")
async def notifications():
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    notifications = await Notification.filter(user=user).order_by("-id")

    return render_template("notifications.html", logged_in=user, notifications=notifications)

@turfie.route("/notification/read/<int:notificationid>/")
async def read_notification(notificationid: int):
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    notification = await Notification.get(id=notificationid)
    notuser = await notification.user.get()
    if notuser.id != user.id:
        return redirect(url_for("turfie.dashboard", error="You are not allowed to read this notification"))

    await notification.read()

    return "success"

@turfie.route("/joinrequest/<int:joinrequestid>", methods=["GET", "POST"])
async def joinrequest(joinrequestid: int):
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    joinrequest = await JoinRequest.get(id=joinrequestid)
    joinuser = await joinrequest.user.get()
    group = await joinrequest.group.get()
    admin = await group.admin.get()
    admin = admin.id == user.id

    if request.method == "POST":
        if not admin:
            return redirect(url_for("turfie.dashboard", error="You are not allowed to accept this join request"))

        if request.form["action"] == "decline":
            await joinrequest.deny()
            return redirect(url_for("turfie.dashboard", message="Join request declined"))

        await joinrequest.approve()
        return redirect(url_for("turfie.dashboard", message="Join request accepted"))

    return render_template("joinrequest.html", logged_in=user, admin=admin, joinuser=joinuser, group=group)

@turfie.route("/group/<int:groupid>/members")
async def manage_group(groupid: int):
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))
    
    group = await Group.get(id=groupid)
    admin = await group.admin.get()
    admin = admin.id == user.id

    if not admin:
        return redirect(url_for("turfie.dashboard", error="You are not allowed to manage this group"))
    
    joinrequests = await JoinRequest.filter(group=group).order_by("-id")
    
    finalrequests = []

    for request in joinrequests:
        user = await request.user.get()
        finalrequests.append({"request": request, "user": user})

    gusers = await group.users.all()
    return render_template("managegroup.html", logged_in=user, group=group, gusers=gusers, joinrequests=finalrequests)

@turfie.route("/group/<int:groupid>/removemember/<int:userid>")
async def remove_member(groupid: int, userid: int):
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))
    
    group = await Group.get(id=groupid)
    admin = await group.admin.get()

    if not admin.id == user.id:
        return redirect(url_for("turfie.dashboard", error="You are not allowed to manage this group"))
    
    guser = await User.get(id=userid)

    if guser.id == admin.id:
        return redirect(url_for("turfie.dashboard", error="You are not allowed to remove yourself from the group"))
    
    await group.users.remove(guser)

    return redirect(url_for("turfie.manage_group", groupid=groupid))

@turfie.route("/joingroup")
async def join_group():
    user = await  check_if_logged_in()

    if not user:
        return redirect(url_for("turfie.login"))

    groups = await Group.all()

    return render_template("joingroup.html", logged_in=user, groups=groups)