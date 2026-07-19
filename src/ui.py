import cv2
import time
import numpy as np
# --------------------------------------
# FPS Counter
# ---------------------------------------
_prev_time = time.time()


def draw_fps(frame):
    global _prev_time

    current_time = time.time()

    fps = 1 / (current_time - _prev_time)

    _prev_time = current_time

    cv2.putText(
    frame,
    f"FPS: {fps:.1f}",
    (20, 70),      # Move below Hands
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 0),
    2,
)

def draw_steering_gauge(frame, angle):

    center = (520, 350)
    radius = 70

    # Outer circle
    cv2.circle(frame, center, radius, (255, 255, 255), 2)

    # Inner circle
    cv2.circle(frame, center, 6, (255, 255, 255), -1)

    # Clamp angle
    angle = max(-90, min(90, angle))

    # Convert to radians
    theta = np.radians(-angle - 90)

    x = int(center[0] + radius * np.cos(theta))
    y = int(center[1] + radius * np.sin(theta))

    # Needle
    cv2.line(frame, center, (x, y), (0, 255, 255), 3)

    cv2.putText(
        frame,
        "STEERING",
        (center[0] - 45, center[1] + 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"{angle:.1f} deg",
        (center[0] - 30, center[1] + 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        2,
    )

# ---------------------------------------
# Steering Bar
# ---------------------------------------
def draw_steering_bar(frame, angle):

    angle = max(-90, min(90, angle))

    start_x = 20
    start_y = 330
    width = 300
    height = 20

    # Draw outer box
    cv2.rectangle(
        frame,
        (start_x, start_y),
        (start_x + width, start_y + height),
        (255, 255, 255),
        2,
    )

    # Center line
    center = start_x + width // 2
    cv2.line(
        frame,
        (center, start_y),
        (center, start_y + height),
        (255, 255, 255),
        2,
    )

    # Scale angle to pixels
    offset = int((-angle / 90) * (width // 2))

    if offset < 0:
        # LEFT (green)
        cv2.rectangle(
            frame,
            (center + offset, start_y),
            (center, start_y + height),
            (0, 255, 0),
            -1,
        )

    elif offset > 0:
        # RIGHT (red)
        cv2.rectangle(
            frame,
            (center, start_y),
            (center + offset, start_y + height),
            (0, 0, 255),
            -1,
        )

    cv2.putText(
        frame,
        "LEFT",
        (start_x, start_y + 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        "RIGHT",
        (start_x + width - 55, start_y + 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
# ---------------------------------------
# Steering Wheel
# ---------------------------------------
def draw_virtual_wheel(frame, center1, center2):

    midpoint = (
        (center1[0] + center2[0]) // 2,
        (center1[1] + center2[1]) // 2,
    )

    radius = int(
        (
            (center1[0] - center2[0]) ** 2
            + (center1[1] - center2[1]) ** 2
        ) ** 0.5
        / 2
    )

    cv2.circle(
        frame,
        midpoint,
        radius,
        (255, 0, 255),
        2,
    )

    cv2.circle(
        frame,
        center1,
        10,
        (255, 0, 0),
        -1,
    )

    cv2.circle(
        frame,
        center2,
        10,
        (255, 0, 0),
        -1,
    )

    cv2.line(
        frame,
        center1,
        center2,
        (0, 255, 255),
        4,
    )


# ---------------------------------------
# Steering Percentage
# ---------------------------------------
def steering_percentage(angle):

    angle = max(-90, min(90, angle))

    percentage = abs(angle) / 90 * 100

    DEAD_ZONE = 10

    if angle < -DEAD_ZONE:
        direction = "Right"

    elif angle > DEAD_ZONE:
        direction = "Left"

    else:
        direction = "STRAIGHT"
        percentage = 0

    return direction, int(percentage)

def draw_dashboard(frame):
    """
    Draws a semi-transparent dashboard panel.
    """

    overlay = frame.copy()

    x, y = 10, 10
    w, h = 320, 340

    # Background
    cv2.rectangle(
        overlay,
        (x, y),
        (x + w, y + h),
        (30, 30, 30),
        -1,
    )

    alpha = 0.55
    cv2.addWeighted(
        overlay,
        alpha,
        frame,
        1 - alpha,
        0,
        frame,
    )

    # Border
    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        (255, 255, 255),
        2,
    )

    # Title
    cv2.putText(
        frame,
        "DRIVER DASHBOARD",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )
def draw_dashboard(frame):

    overlay = frame.copy()

    x = 10
    y = 10
    width = 320
    height = 260

    # Semi-transparent background
    cv2.rectangle(
        overlay,
        (x, y),
        (x + width, y + height),
        (20, 20, 20),
        -1,
    )

    cv2.addWeighted(
        overlay,
        0.6,
        frame,
        0.4,
        0,
        frame,
    )

    # Border
    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (255, 255, 255),
        2,
    )

    # Title
    cv2.putText(
        frame,
        "DRIVER DASHBOARD",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    # Divider
    cv2.line(
        frame,
        (20, 55),
        (320, 55),
        (120, 120, 120),
        1,
    )
def draw_dashboard_info(
    frame,
    hands,
    fps,
    gesture,
    steering,
    angle,
    turn,
):

    x = 25
    y = 85

    font = cv2.FONT_HERSHEY_SIMPLEX

    info = [
        ("Hands", hands),
        ("FPS", f"{fps:.1f}"),
        ("Gesture", gesture),
        ("Steering", steering),
        ("Angle", f"{angle:.1f}°"),
        ("Turn", f"{turn}%"),
    ]

    for label, value in info:

        cv2.putText(
            frame,
            f"{label:<10}: {value}",
            (x, y),
            font,
            0.65,
            (255, 255, 255),
            2,
        )

        y += 30