import cv2
import time

def show_alert(frame, message):

    cv2.putText(
        frame,
        message,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

def save_screenshot(frame):

    filename = f"reports/cheating_{int(time.time())}.jpg"

    cv2.imwrite(
        filename,
        frame
    )