import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ---------------------------------------
# Draw landmarks and IDs
# ---------------------------------------
def draw_landmarks(frame, detection_result):
    h, w, _ = frame.shape

    for hand_landmarks in detection_result.hand_landmarks:
        for idx, landmark in enumerate(hand_landmarks):

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            cv2.putText(
                frame,
                str(idx),
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1
            )


# ---------------------------------------
# Detect finger states
# ---------------------------------------
def get_finger_states(hand_landmarks):

    fingers = {}

    finger_pairs = {
        "Index": (8, 6),
        "Middle": (12, 10),
        "Ring": (16, 14),
        "Pinky": (20, 18),
    }

    for finger, (tip, joint) in finger_pairs.items():
        fingers[finger] = hand_landmarks[tip].y < hand_landmarks[joint].y

    return fingers


# ---------------------------------------
# Gesture Recognition
# ---------------------------------------
def recognize_gesture(fingers):

    index = fingers["Index"]
    middle = fingers["Middle"]
    ring = fingers["Ring"]
    pinky = fingers["Pinky"]

    if index and middle and ring and pinky:
        return "OPEN PALM"

    if not index and not middle and not ring and not pinky:
        return "FIST"

    if index and not middle and not ring and not pinky:
        return "POINTING"

    return "UNKNOWN"


# ---------------------------------------
# Load Hand Landmarker
# ---------------------------------------
base_options = python.BaseOptions(
    model_asset_path="models/hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(options)

print("✅ Hand Landmarker loaded successfully!")


# ---------------------------------------
# Webcam
# ---------------------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("✅ Webcam started. Press Q to quit.")


# ---------------------------------------
# Main Loop
# ---------------------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms = int(time.time() * 1000)

    result = detector.detect_for_video(mp_image, timestamp_ms)

    draw_landmarks(frame, result)

    hand_count = len(result.hand_landmarks)

    cv2.putText(
        frame,
        f"Hands: {hand_count}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if hand_count > 0:

        hand_landmarks = result.hand_landmarks[0]

        fingers = get_finger_states(hand_landmarks)

        gesture = recognize_gesture(fingers)

        y = 70

        for finger, state in fingers.items():

            text = f"{finger}: {'Open' if state else 'Closed'}"

            cv2.putText(
                frame,
                text,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 0),
                2
            )

            y += 30

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (20, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    cv2.imshow("Virtual Steering Wheel", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()