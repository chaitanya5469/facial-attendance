from datetime import datetime

import firebase_admin
from firebase_admin import credentials, db

"""# FireBase DataBase Credentials"""
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://face-attendance-f018e-default-rtdb.firebaseio.com/"})
ref = db.reference("Users")

"""# Save the data to database in form of a dictionary to the database"""


def register_user_to_db(name, rollno):
    data = {
        "name": name,
        "rollno": rollno,
        "total_attendance": 0,
        "last_attendance": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    ref.child(rollno).set(data)


# retrieve the data from the database as a dictionary
def get_user_data(rollno):
    return ref.child(rollno).get()


# update the attendance to database in form of a dictionary to the database when user login
def login_user_db(rollno, total_attendance: int):
    data = {
        "total_attendance": total_attendance,
        "last_attendance": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ref.child(rollno).update(data)
