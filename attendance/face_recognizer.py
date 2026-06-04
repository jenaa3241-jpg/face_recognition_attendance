import cv2
import os
import numpy as np

from students.models import Student

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

MODEL_PATH = "trained_model.yml"


def train_model():

    faces = []
    labels = []

    students = Student.objects.all()

    for student in students:

        if not student.photo:
            continue

        img = cv2.imread(student.photo.path)

        if img is None:
            continue

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        detected = face_detector.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in detected:

            faces.append(
                gray[y:y+h, x:x+w]
            )

            labels.append(
                student.id
            )

    if len(faces):

        recognizer.train(
            faces,
            np.array(labels)
        )

        recognizer.save(
            MODEL_PATH
        )


def recognize_student(frame):

    if not os.path.exists(MODEL_PATH):
        train_model()

    recognizer.read(
        MODEL_PATH
    )

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        1.3,
        5
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        match_percent = 100 - confidence

        if match_percent >= 70:

            try:

                student = Student.objects.get(
                    id=label
                )

                return (
                    student,
                    match_percent,
                    (x, y, w, h)
                )

            except:
                pass

    return None, 0, None