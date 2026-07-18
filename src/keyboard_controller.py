from pynput.keyboard import Controller, Key

keyboard = Controller()

left_pressed = False
right_pressed = False


def update_keyboard(direction):
    global left_pressed, right_pressed

    if direction == "LEFT":

        if right_pressed:
            keyboard.release("d")
            right_pressed = False

        if not left_pressed:
            keyboard.press("a")
            left_pressed = True

    elif direction == "RIGHT":

        if left_pressed:
            keyboard.release("a")
            left_pressed = False

        if not right_pressed:
            keyboard.press("d")
            right_pressed = True

    else:

        if left_pressed:
            keyboard.release("a")
            left_pressed = False

        if right_pressed:
            keyboard.release("d")
            right_pressed = False


def release_all():
    global left_pressed, right_pressed

    if left_pressed:
        keyboard.release("a")

    if right_pressed:
        keyboard.release("d")

    left_pressed = False
    right_pressed = False