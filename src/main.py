import cv2

from ui import (
    draw_fps,
    draw_steering_bar,
    draw_virtual_wheel,
    steering_percentage,
    draw_dashboard,
    draw_dashboard_info,
    draw_steering_gauge,
)

from hand_detector import HandDetector
from gesture import get_finger_states, recognize_gesture
from steering import (
    get_hand_center,
    calculate_angle,
)

from keyboard_controller import (
    update_keyboard,
    release_all,
)

detector = HandDetector()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    result = detector.detect(frame)

    detector.draw_landmarks(frame, result)

    hand_count = len(result.hand_landmarks)

    # -----------------------------
    # Default values
    # -----------------------------
    gesture = "--"
    direction = "STRAIGHT"
    angle = 0.0
    percent = 0

    # -----------------------------
    # Single Hand
    # -----------------------------
    if hand_count >= 1:

        fingers = get_finger_states(result.hand_landmarks[0])

        gesture = recognize_gesture(fingers)

        y = 70

        for finger, state in fingers.items():

            cv2.putText(
                frame,
                f"{finger}: {'Open' if state else 'Closed'}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2,
            )

            y += 30

    # -----------------------------
    # Two Hands
    # -----------------------------
    if hand_count == 2:

        center1 = get_hand_center(
            result.hand_landmarks[0],
            frame,
        )

        center2 = get_hand_center(
            result.hand_landmarks[1],
            frame,
        )

        draw_virtual_wheel(
            frame,
            center1,
            center2,
        )

        angle = calculate_angle(
            center1,
            center2,
        )

        draw_steering_bar(
            frame,
            angle,
        )

        direction, percent = steering_percentage(angle)

        update_keyboard(direction)

        midpoint = (
            (center1[0] + center2[0]) // 2,
            (center1[1] + center2[1]) // 2,
        )

        cv2.putText(
            frame,
            f"Angle : {angle:.1f}°",
            midpoint,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

    else:
        release_all()

    # -----------------------------
    # Dashboard
    # -----------------------------
    draw_dashboard(frame)
    draw_steering_gauge(
    frame,
    angle,
    )
    draw_dashboard_info(
        frame,
        hand_count,
        0,              # FPS (we'll connect this later)
        gesture,
        direction,
        angle,
        percent,
    )

    # -----------------------------
    # FPS
    # -----------------------------
    draw_fps(frame)

    cv2.imshow(
        "Virtual Steering Wheel",
        frame,
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

release_all()

cap.release()
cv2.destroyAllWindows()