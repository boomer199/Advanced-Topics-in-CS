import os
import json

#base account information
class Account:
    def __init__(self):
        self.username = self.password = self.salt = "" # look at that one liner 


class Profile:
    def __init__(self):
        # start with nothing, build ur empire of files later
        self.username = self.fname = self.lname = self.files = ""
        self.avatar = "avatars/default_avatar.jpg"  # cuz everyone starts as a duck named deck

    def jsonify(self):
        return {"username": self.username, "fname": self.fname, "lname": self.lname, "avatar": self.avatar, "files": self.files}

    def __str__(self):
        return json.dumps(self.jsonify())
