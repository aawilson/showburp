Welcome to a stupid test app for showing a reasonable Burp interception use!

BEFORE ANYONE WHO MIGHT SEE THIS COMPLAINS: This is purposefully ignoring some secure best-practices, and doesn't care about others, so don't sweat them if you see them.

This is a web app that allows stupid simple login and password resets. To get it up and running:

1. Set up your environment the way you want (maybe get a virtualenv and enter it)
2. `pip install -r requirements.txt`
3. Edit `populate_users.py` if you want usernames and passwords that aren't in there
4. Run `python populate_users.py` (you can remove `tutorial.db` and do this step again to refresh the db for whatever reason)
5. Run `python main.py`, navigate to localhost:4000
