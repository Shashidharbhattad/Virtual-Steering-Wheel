import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:
    def __init__(self):
        base_options = python.BaseOptions(
            model_asset_path="models/hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp = int(time.time() * 1000)

        return self.detector.detect_for_video(
            mp_image,
            timestamp
        )

    def draw_landmarks(self, frame, result):

        h, w, _ = frame.shape

        for hand in result.hand_landmarks:

            for idx, landmark in enumerate(hand):

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0,255,0),
                    -1
                )

                cv2.putText(
                    frame,
                    str(idx),
                    (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (255,255,255),
                    1
                )