import tkinter
import pickle
from datetime import datetime
from tkinter import *
import cv2
import face_recognition
from PIL import ImageTk, Image
import os
import firebase_db
import util


class App:
    def __init__(self):
        """initialise the main window and set the title and geometry"""
        self.main_window = Tk()
        self.main_window.title("FACIAL ATTENDANCE")
        self.main_window.geometry("1500x600")

        """load the background image of main window"""
        bg = PhotoImage(file="face.png")
        self.bg_label = util.get_img_label(self.main_window)
        self.bg_label.imgtk = bg
        self.bg_label.configure(image=bg)
        self.bg_label.pack()

        """create graphics and user interface by adding buttons"""
        self.main_window_login_btn = util.get_button(self.main_window, "LOGIN", "blue", self.login)
        self.main_window_login_btn.place(x=50, y=500)
        self.main_window_register_btn = util.get_button(self.main_window, "REGISTER", "green", self.register)
        self.main_window_register_btn.place(x=320, y=500)
        """"# create a label for displaying camera"""
        self.camera = util.get_img_label(self.main_window)
        self.camera.place(x=30, y=24, width=580, height=450)
        """call the function to open camera"""
        self.startCamera()

        """create a folder to store the .pickle files which store the face encodings"""
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def startCamera(self):
        self.front_cam = cv2.VideoCapture(0)
        self.process_webcam()

    def process_webcam(self):
        """ # read the camera frames into the recent_capture_arr array"""
        res, self.recent_capture_arr = self.front_cam.read()
        """# convert the format from BGR format to RGB format using cv2"""
        img_ = cv2.cvtColor(self.recent_capture_arr, cv2.COLOR_BGR2RGB)
        """# Change the formant to PIL format which is usable by tkinter"""
        self.recent_capture_arr_pil = Image.fromarray(img_)
        """ # Convert the image format again to tkinter format and load into camera label
        # Call the same function every 20ms to continuously update the camera label"""
        image = ImageTk.PhotoImage(image=self.recent_capture_arr_pil)
        self.camera.imgtk = image
        self.camera.configure(image=image)

        self.camera.after(20, self.process_webcam)

    """# login function compares the array of most recent captured frame to .pickle files in the db folder
    # if there is a match then it updates the total attendance and last attendance time in the database
    # otherwise it shows unknown person or no person found
    # Also it checks whether the user logged in the last 24 hours. if he logged in then it doesn't update database
    # it displays another window for displaying logged-in user details"""

    def login(self):
        rollno = util.recognize(self.recent_capture_arr, self.db_dir)
        if rollno == "unknown_person":
            util.msg_box_error('Oops...', 'Unknown user. Please register or try again.')
        elif rollno == "no_persons_found":
            util.msg_box_error('Oops...', "Can't recognize any person")
        else:
            student_data = firebase_db.get_user_data(rollno)
            name = student_data["name"]
            total_attendance = student_data["total_attendance"]
            last_attendance_time = student_data["last_attendance"]
            time_stamp_last = datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
            self.logged_in_window = tkinter.Toplevel(self.main_window)
            self.logged_in_window.title("Welcome {}".format(name))
            self.logged_in_window.geometry("750x450+400+200")
            bg = PhotoImage(file="bg.png")
            self.bg_label = util.get_img_label(self.logged_in_window)
            self.bg_label.imgtk = bg
            self.bg_label.configure(image=bg)
            self.bg_label.pack()
            self.logged_in_window_title = util.get_text_label(self.logged_in_window, "Welcome {}".format(name))
            self.logged_in_window_title.place(x=240, y=90)
            self.logged_in_window_roll = util.get_text_label(self.logged_in_window, "Roll no {}".format(rollno))
            self.logged_in_window_roll.place(x=240, y=155)

            secondsElapsed = (datetime.now() - time_stamp_last).total_seconds()
            if secondsElapsed > 60:
                firebase_db.login_user_db(rollno, total_attendance + 1)
                self.logged_in_window_attendance = util.get_text_label(self.logged_in_window,
                                                                       "Total Attendance : {} Days".format(
                                                                           str(total_attendance + 1)))
                self.info_msg = util.get_text_label(self.logged_in_window,
                                                    "Attendance successfully marked at {}"
                                                    .format(datetime.now().strftime("%Y-%M-%D %H:%M")))
            else:
                self.logged_in_window_attendance = util.get_text_label(self.logged_in_window,
                                                                       "Total Attendance : {} Days".format(
                                                                           total_attendance))
                self.info_msg = util.get_text_label(self.logged_in_window,
                                                    "Attendance already marked at {}"
                                                    .format(last_attendance_time))
            self.logged_in_window_attendance.place(x=200, y=220)
            self.info_msg.place(x=50, y=300)
        pass

    """# displays the main window on loop"""

    def start(self):
        self.main_window.mainloop()

    """# it loads the camera frames into another label in the registration window"""

    def add_new_cam(self):
        image = ImageTk.PhotoImage(image=self.recent_capture_arr_pil)
        self.camera_register.imgtk = image
        self.camera_register.configure(image=image)

        self.camera_register.after(20, self.add_new_cam)

    """# register function asks user to take a good selfie. it then captures the image amd calls done() function"""

    def register(self):
        self.register_window_1 = tkinter.Toplevel(self.main_window)
        self.register_window_1.geometry("710x650+150+100")
        self.info_text = util.get_text_label(self.register_window_1, "Take a good selfie")
        self.info_text.place(x=250, y=480)
        self.accept = util.get_button(self.register_window_1, "Done", "blue", self.done)
        self.accept.place(x=230, y=530)
        self.camera_register = util.get_img_label(self.register_window_1)
        self.camera_register.place(x=30, y=24, width=650, height=450)
        self.add_new_cam()

    """  # it displays a new window and ask user to enter name and roll no.
    # it also displays the selfie taken by user in last window.
    # it goes to the last window when try again is clicked.
    # it saves the data to the database using register_user_to_db in the firebase_db file."""

    def done(self):
        self.register_window_1.destroy()
        self.register_window_2 = tkinter.Toplevel(self.main_window)
        self.register_window_2.geometry("1200x510+150+100")
        bg = PhotoImage(file="bg.png")
        self.bg_label = util.get_img_label(self.register_window_2)
        self.bg_label.imgtk = bg
        self.bg_label.configure(image=bg)
        self.bg_label.pack()
        self.captured_image = util.get_img_label(self.register_window_2)
        self.captured_image.place(x=50, y=30, width=580, height=450)
        image = ImageTk.PhotoImage(image=self.recent_capture_arr_pil)
        self.captured_image.imgtk = image
        self.captured_image.configure(image=image)
        self.register_user_capture_arr = self.recent_capture_arr.copy()
        self.entry_name_register_new_user = util.get_entry_text(self.register_window_2)
        self.entry_name_register_new_user.place(x=750, y=170)
        self.entry_rollno_register_new_user = util.get_entry_text(self.register_window_2)
        self.entry_rollno_register_new_user.place(x=750, y=300)
        self.text_label_register_new_user = util.get_text_label(self.register_window_2,
                                                                'Please, input username:')
        self.text_label_register_new_user.place(x=750, y=120)
        self.text_label_register_new_user_rollno = util.get_text_label(self.register_window_2,
                                                                       'Please, input rollno:')
        self.text_label_register_new_user_rollno.place(x=750, y=250)
        self.accept_button_register_new_user_window = util.get_button(self.register_window_2, 'Accept', 'green',
                                                                      self.register_user_in_db)
        self.accept_button_register_new_user_window.place(x=650, y=400)

        self.try_again_button_register_new_user_window = util.get_button(self.register_window_2, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=920, y=400)

    """# it converts the image into encodings and write it to a .pickle file."""

    def register_user_in_db(self):
        name = self.entry_name_register_new_user.get(1.0, "end-1c")
        rollno = self.entry_rollno_register_new_user.get(1.0, "end-1c")
        embeddings = face_recognition.face_encodings(self.register_user_capture_arr)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(rollno)), 'wb')

        pickle.dump(embeddings, file)
        firebase_db.register_user_to_db(name, rollno)

        self.register_window_2.destroy()
        util.msg_box_info('Success!', 'User was registered successfully !')

    def try_again_register_new_user(self):
        self.register_window_2.destroy()
        self.register()


app = App()
app.start()
