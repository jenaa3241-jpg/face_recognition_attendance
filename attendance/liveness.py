import cv2

eye_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_eye.xml"
)


def is_live_face(frame):

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    eyes = eye_detector.detectMultiScale(
        gray
    )

    return len(eyes) >= 2