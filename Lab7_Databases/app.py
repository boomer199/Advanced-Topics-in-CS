from flask import Flask, redirect, send_file, request, render_template
from db import session_get, session_set, session_delete, account_auth, profile_get, account_create, account_update_password, profile_update, profile_delete
import os

app = Flask(__name__)

# err msgs (self explanatory)
ERROR_MESSAGES = {
    1: "incorrect username or password",
    2: "username already exists",
    3: "invalid request",
    4: "not logged in",
    "default": "please try again"
}

@app.route("/")
def home():
    # get token, if it exists cool, if not lol
    token, prof = request.cookies.get("token"), None
    if token:
        prof = session_get(token)
    if not token or not prof:
        resp = redirect("/login") # no token? go login
        if not token and prof:
            resp.set_cookie("token", "", max_age=0) #expire token
        return resp
    return redirect(f"/{prof.username}/profile") # profile exists we go


#login route handles registration too!
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        mode, username, password = request.form.get("mode"), request.form.get("username"), request.form.get("password")
        if mode == "login":
            #authorize login (no hackers!!!)
            if account_auth(username, password):
                prof, token = profile_get(username), session_set(profile_get(username))
                resp = redirect(f"/{username}/profile")# go to profile :D
                resp.set_cookie("token", token)#make new token
                return resp
            return render_template("login.j2", error_message=ERROR_MESSAGES[1])
        elif mode == "register":
            #make new acc
            if profile_get(username) is not None:
                return render_template("login.j2", error_message=ERROR_MESSAGES[2])
            prof, token = account_create(username, password), session_set(account_create(username, password))
            resp = redirect(f"/{username}/profile")
            resp.set_cookie("token", token)
            return resp
        return "FAILURE" # if all else fails, just fail
    return render_template("login.j2", error_message=None) # that didn't work, register again!!!!!!



@app.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token")
    if token:
        session_delete(token)# delete token from session
    resp = redirect("/") # set up response
    resp.set_cookie("token", "", max_age=0)
    return resp


#ty lucas for help here (kinda stole code)
@app.route("/<user>/profile", methods=["POST", "GET"])
def user_profile(user):
    # check if you're even supposed to be here
    token = request.cookies.get("token")
    is_logged_in = token != None

    if is_logged_in:
        profile = session_get(token) #get from redis (active profile)
        if profile == None:
            #gotta log in first lmao
            return render_template("login.j2", error_message=ERROR_MESSAGES[4])
    else:
        return render_template("login.j2", error_message=ERROR_MESSAGES[4])

    if request.method == "GET":
        is_personal_profile = True # assuming it's ur profile at first

        # if ur sneaking into someone else's profile
        if profile.username != user:
            profile = profile_get(user)
            is_personal_profile = False # haha no getting to other peoples profiles 

        if profile == None:
            return redirect("/") #profile in URL doesn't exist
        #load profile if real person
        return render_template("profile.j2", profile=profile, files=os.listdir(profile.files), show_options=is_personal_profile)
    else:
        #editing profile logic
        action = request.form.get("action")

        if action == "password":
            new_password = request.form.get("new_password")  
            success = account_update_password(user, new_password)  # new pwd, don't forget it lmao
            
            
        elif action == "picture":
            picture = request.files["picture"]

            ext = picture.filename.split(".")[1] #get file type (i.e. png, jpg, etc.)
            new_loc = os.path.join("static/avatars/", "".join([user, ".", ext]))

            picture.save(new_loc) #save locally
            #update the profile to show off the picture
            profile_update(token=token, username=user, avatar=os.path.join("avatars/", "".join([user, ".", ext])))
            
        #in case you have a name
        elif action == "name":
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            profile_update(token=token, username=user, fname=fname, lname=lname)
            
            
            
        elif action == "delete":
            confirmation = request.form.get("confirmation")
            if confirmation == user:
                # big goodbye, delete everything
                profile_delete(user)
                session_delete(token)

                resp = redirect("/login")
                resp.set_cookie("token", "", max_age=0)  # Delete cookie
                return resp

        # grab ur updated profile, see the changes
        profile = session_get(token) 
        
        
        # show off ur profile, now with updates (gotta log out and log back in for no reason ig)
        return render_template("profile.j2", profile=profile, files=os.listdir(profile.files), show_options=True)


@app.route("/<user>/files", methods=["POST"])
def user_files(user):
    pass

if __name__ == "__main__":
    app.run(port=8022)


