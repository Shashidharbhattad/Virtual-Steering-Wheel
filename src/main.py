import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ----------------------------
# Load Hand Landmarker Model
# ----------------------------
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

# ----------------------------
# Open Webcam
# ----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("✅ Webcam started. Press Q to quit.")

# ----------------------------
# Show Webcam
# ----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Virtual Steering Wheel", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()