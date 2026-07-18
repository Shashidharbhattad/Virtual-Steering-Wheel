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

            # Draw landmark
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Draw landmark ID
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
# Open Webcam
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

    # Mirror image
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Timestamp
    timestamp_ms = int(time.time() * 1000)

    # Detect hands
    result = detector.detect_for_video(mp_image, timestamp_ms)

    # Draw landmarks
    draw_landmarks(frame, result)

    # Display number of hands
    hand_count = len(result.hand_landmarks)

    cv2.putText(
        frame,
        f"Hands: {hand_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show frame
    cv2.imshow("Virtual Steering Wheel", frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()