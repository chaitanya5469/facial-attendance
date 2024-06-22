# Facial Attendance Desktop App

## Overview

This is a Python-based facial attendance system developed as a college python project. The application uses facial recognition to mark attendance, leveraging a Firebase database to store details such as the number of days attendance was marked, the last time it was marked, and the student's name and roll number. The graphical user interface (GUI) is built using Tkinter.

## Features

- **Login and Registration**: Users can log in or register using their facial images.
- **Face Detection and Recognition**: Utilizes OpenCV and Face Recognition libraries to detect and recognize faces.
- **Attendance Marking**: Marks attendance by comparing the user's face encoding with the database records.
- **Image Processing**: Processes images using the Pillow library.
- **Database Integration**: Stores and retrieves data from Firebase or local files.

## Libraries Used

- **OpenCV**: Computer vision library based on machine learning.
- **Face Recognition**: Library for face detection, recognition, and identification.
- **Pillow**: Python Imaging Library used for image processing.
- **Tkinter**: Python library for creating GUI.
- **Pickle**: Converts objects into binary data and vice versa, allowing objects to be stored in and loaded from files.

## Database

- **Firebase**: Used to store user login data and attendance details.
- **Local Files**: Used as a fallback option if Firebase is not available.

## Functionality

1. **Login**:
   - User clicks the login button.
   - The current face image of the user is captured.
   - The image is converted to a face encoding using OpenCV and Face Recognition Library.
   - The face encoding is compared with all face encodings in the database.
   - If a match is found, attendance is marked in the database.
   - If no match is found, the user is prompted with a screen with two buttons: Register and Try Again.
   
2. **Register**:
   - User clicks the register button.
   - Instructions are displayed (e.g., "Ensure your face is clear...").
   - The user's face image is captured and converted into an encoding.
   - User inputs their name.
   - The user's name and encoding are stored in the database.

3. **Optional Functionality**:
   - If a user attempts to log in more than once in a day, an error screen is displayed.
   - This requires storing the login time in the database.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/facial-attendance-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd facial-attendance-app
   ```
3. Install the required libraries:
   ```bash
   pip install opencv-python face-recognition Pillow firebase-admin
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Use the GUI to register or log in:
   - **Login**: Click the login button to capture your face image and mark attendance.
   - **Register**: Click the register button to capture your face image and store your details.

## Notes

- Ensure that your webcam is properly connected and functioning.
- Make sure to have a stable internet connection if using Firebase as the database.
- The accuracy of facial recognition may vary based on lighting conditions and image quality.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to this project by submitting issues or pull requests. Your feedback is valuable!

**Project Maintainer**: [Ch Chaitanya Krishna] (chaitudec2005@gmail.com)