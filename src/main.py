import cv2

from hand_detector import HandDetector
from gesture import get_finger_states, recognize_gesture
from steering import (
    get_hand_center,
    calculate_angle,
    steering_direction,
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

    cv2.putText(
        frame,
        f"Hands : {hand_count}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

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

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (20, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    if hand_count == 2:

        center1 = get_hand_center(
            result.hand_landmarks[0],
            frame,
        )

        center2 = get_hand_center(
            result.hand_landmarks[1],
            frame,
        )

        cv2.circle(frame, center1, 12, (255, 0, 0), -1)
        cv2.circle(frame, center2, 12, (255, 0, 0), -1)

        cv2.line(
            frame,
            center1,
            center2,
            (0, 255, 255),
            4,
        )

        angle = calculate_angle(center1, center2)

        direction = steering_direction(angle)

        update_keyboard(direction)

        midpoint = (
            (center1[0] + center2[0]) // 2,
            (center1[1] + center2[1]) // 2,
        )

        cv2.putText(
            frame,
            f"Angle : {angle}",
            midpoint,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Steering : {direction}",
            (20, 260),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2,
        )

    else:
        release_all()

    cv2.imshow("Virtual Steering Wheel", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

release_all()

cap.release()
cv2.destroyAllWindows()