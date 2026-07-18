import math

smoothed_angle = 0


def get_hand_center(hand_landmarks, frame):
    h, w, _ = frame.shape

    wrist = hand_landmarks[0]

    x = int(wrist.x * w)
    y = int(wrist.y * h)

    return (x, y)


def calculate_angle(left_hand, right_hand):
    global smoothed_angle

    dx = right_hand[0] - left_hand[0]
    dy = right_hand[1] - left_hand[1]

    angle = math.degrees(math.atan2(dy, dx))

    alpha = 0.2
    smoothed_angle = alpha * angle + (1 - alpha) * smoothed_angle

    return int(smoothed_angle)


def steering_direction(angle):

    if angle < -15:
        return "LEFT"

    elif angle > 15:
        return "RIGHT"

    return "STRAIGHT"