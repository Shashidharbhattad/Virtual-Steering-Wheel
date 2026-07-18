def get_finger_states(hand):

    fingers = {}

    finger_pairs = {
        "Index": (8, 6),
        "Middle": (12, 10),
        "Ring": (16, 14),
        "Pinky": (20, 18),
    }

    for finger, (tip, joint) in finger_pairs.items():
        fingers[finger] = hand[tip].y < hand[joint].y

    return fingers


def recognize_gesture(fingers):

    if all(fingers.values()):
        return "OPEN PALM"

    if not any(fingers.values()):
        return "FIST"

    if (
        fingers["Index"]
        and not fingers["Middle"]
        and not fingers["Ring"]
        and not fingers["Pinky"]
    ):
        return "POINTING"

    return "UNKNOWN"