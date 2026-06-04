import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    providers=['CPUExecutionProvider']
)

app.prepare(ctx_id=0)


def get_face_embedding(frame):

    faces = app.get(frame)

    if len(faces) == 0:
        return None

    face = faces[0]

    return face.embedding