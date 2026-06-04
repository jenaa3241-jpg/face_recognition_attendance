import cv2
import os


from datetime import datetime

from django.conf import settings

from deepface import DeepFace

from students.models import Student
from attendance.models import Attendance


MIN_CONFIDENCE = 60


def start_attendance():

    students_folder = os.path.join(
        settings.MEDIA_ROOT,
        "students"
    )

    attendance_folder = os.path.join(
        settings.MEDIA_ROOT,
        "attendance"
    )

    os.makedirs(
        attendance_folder,
        exist_ok=True
    )

    if not os.path.exists(students_folder):
        print("Students folder not found")
        return False

    students = Student.objects.exclude(
        photo=""
    )

    if not students.exists():
        print("No students registered")
        return False

    print("Loading ArcFace Model...")

    DeepFace.build_model(
        "ArcFace"
    )

    print("ArcFace Loaded")

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        640
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        480
    )

    if not cap.isOpened():
        print("Camera not found")
        return False

    temp_image = os.path.join(
        settings.MEDIA_ROOT,
        "temp_live.jpg"
    )

    frame_counter = 0

    print("Attendance Camera Started")

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_counter += 1

        display_frame = frame.copy()

        cv2.putText(
            display_frame,
            "AI ATTENDANCE SYSTEM",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.putText(
            display_frame,
            "Show Face To Camera",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "AI Attendance System",
            display_frame
        )

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

        # Process every 10th frame
        if frame_counter % 10 != 0:
            continue

        cv2.imwrite(
            temp_image,
            frame
        )

        try:

            faces = DeepFace.extract_faces(
                img_path=temp_image,
                detector_backend="retinaface",
                anti_spoofing=True,
                enforce_detection=False
            )

            if len(faces) == 0:
                continue

            for face in faces:

                facial_area = face["facial_area"]

                x = facial_area["x"]
                y = facial_area["y"]
                w = facial_area["w"]
                h = facial_area["h"]

                is_real = face.get(
                    "is_real",
                    True
                )

                if not is_real:

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        frame,
                        "SPOOF DETECTED",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                    cv2.imshow(
                        "AI Attendance System",
                        frame
                    )

                    continue

                best_student = None
                best_confidence = 0

                for student in students:

                    try:

                        if not student.photo:
                            continue

                        registered_image = (
                            student.photo.path
                        )

                        if not os.path.exists(
                            registered_image
                        ):
                            continue

                        result = DeepFace.verify(
                            img1_path=temp_image,
                            img2_path=registered_image,
                            model_name="ArcFace",
                            detector_backend="retinaface",
                            enforce_detection=False
                        )

                        confidence = round(
                            (1 - result["distance"]) * 100,
                            2
                        )

                        if (
                            result["verified"]
                            and confidence > best_confidence
                        ):

                            best_student = student
                            best_confidence = confidence

                    except Exception:
                        continue

                if (
                    best_student is None
                    or best_confidence < MIN_CONFIDENCE
                ):
                    continue

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    3
                )

                cv2.rectangle(
                    frame,
                    (x, y - 90),
                    (x + 420, y),
                    (0, 255, 0),
                    cv2.FILLED
                )

                cv2.putText(
                    frame,
                    f"Name: {best_student.name}",
                    (x + 10, y - 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID: {best_student.student_id}",
                    (x + 10, y - 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Confidence: {best_confidence:.2f}%",
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                today = datetime.now().date()

                already_marked = Attendance.objects.filter(
                    student=best_student,
                    date=today
                ).exists()

                if not already_marked:

                    Attendance.objects.create(
                        student=best_student,
                        status="Present"
                    )

                    attendance_image = os.path.join(
                        attendance_folder,
                        f"{best_student.student_id}_{today}.jpg"
                    )

                    cv2.imwrite(
                        attendance_image,
                        frame
                    )

                    cv2.putText(
                        frame,
                        "ATTENDANCE MARKED",
                        (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        3
                    )

                    cv2.imshow(
                        "AI Attendance System",
                        frame
                    )

                    cv2.waitKey(2000)

                    cap.release()
                    cv2.destroyAllWindows()

                    if os.path.exists(
                        temp_image
                    ):
                        os.remove(
                            temp_image
                        )

                    print(
                        f"Attendance Marked : {best_student.name}"
                    )

                    return True

        except Exception as e:
            print(
                "Recognition Error:",
                e
            )

    cap.release()
    cv2.destroyAllWindows()

    if os.path.exists(
        temp_image
    ):
        os.remove(
            temp_image
        )

    return False