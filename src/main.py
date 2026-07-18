import cv2
import mediapipe as mp
import time


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

    # Mirror image
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Timestamp in milliseconds
    timestamp_ms = int(time.time() * 1000)

    # Detect hands
    result = detector.detect_for_video(mp_image, timestamp_ms)

    # Number of hands
    hand_count = len(result.hand_landmarks)

    if hand_count > 0:
        cv2.putText(
            frame,
            f"Hands: {hand_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Virtual Steering Wheel", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break