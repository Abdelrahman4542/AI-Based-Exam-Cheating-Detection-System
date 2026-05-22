import cv2
import mediapipe as mp

from reasoning_engine import analyze_behavior
from alerts import show_alert, save_screenshot
from utils import calculate_score

# --------------------------------
# MediaPipe Setup
# --------------------------------

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --------------------------------
# Open Camera
# --------------------------------

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Flip Frame
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process Face Mesh
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape

    # --------------------------------
    # Behavior Variables
    # --------------------------------

    looking_away = False
    tab_switching = False

    # --------------------------------
    # Eye Tracking
    # --------------------------------

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            left_point = 33
            right_point = 263

            lx = int(face_landmarks.landmark[left_point].x * w)
            ly = int(face_landmarks.landmark[left_point].y * h)

            rx = int(face_landmarks.landmark[right_point].x * w)
            ry = int(face_landmarks.landmark[right_point].y * h)

            # Draw Eye Points
            cv2.circle(frame, (lx, ly), 5, (0, 255, 0), -1)
            cv2.circle(frame, (rx, ry), 5, (0, 255, 0), -1)

            # Looking Away Detection
            if abs(lx - rx) < 100:
                looking_away = True

    # --------------------------------
    # Simulate Tab Switching
    # --------------------------------

    key = cv2.waitKey(1)

    if key == ord('t'):
        tab_switching = True

    # --------------------------------
    # Analyze Behavior
    # --------------------------------

    result = analyze_behavior(
        looking_away,
        tab_switching
    )

    # --------------------------------
    # Calculate Score
    # --------------------------------

    score = calculate_score(looking_away, tab_switching)

    # --------------------------------
    # Show Alert
    # --------------------------------

    show_alert(frame, result)
    # --------------------------------
    # Save Screenshot
    # --------------------------------

    if result == "Suspicious Behavior Detected":

       save_screenshot(frame)
    # --------------------------------   
    # Show Score
    # --------------------------------
    
    cv2.putText(
       frame,
       f"Suspicious Score: {score}",
       (50, 100),
       cv2.FONT_HERSHEY_SIMPLEX,
       1,
       (255, 255, 0),
       2
    )

    # --------------------------------
    # Show Camera
    # --------------------------------

    cv2.imshow(
        "AI Exam Monitoring System",
        frame
    )

    # Exit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()