import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition


# method for creating a tkinter button
def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground=color,
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=18,
        font=('Times New Roman', 20)
    )

    return button


# method for creating an image label
def get_img_label(window):
    label = tk.Label(window)

    return label


# method for creating a text label
def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Times New Roman", 21), justify="left")
    return label


# method for creating input text label
def get_entry_text(window):
    inputtxt = tk.Entry(window,
                       height=1,
                       width=20, font=("Arial", 24))
    return inputtxt


# method for creating message box
def msg_box_info(title, description):
    messagebox.showinfo(title, description)


def msg_box_error(title, description):
    messagebox.showerror(title, description)


# this method generates the encodings of the image and compares
# it with the face encodings stored in the .pickle files listed in db directory
# it then returns the pickle file name if a there is a match otherwise it returns error message


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    encoding_unknown = face_recognition.face_encodings(img)
    if len(encoding_unknown) == 0:
        return 'no_persons_found'
    else:
        encoding_unknown = encoding_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path = os.path.join(db_path, db_dir[j])

        file = open(path, 'rb')
        encoding = pickle.load(file)
        match = face_recognition.compare_faces([encoding], encoding_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'
