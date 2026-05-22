import cv2
import mediapipe as mp

# MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Open Webcam
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Flip Image
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process Face Mesh
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape

    looking_away = False

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # Eye Points
            left_point = 33
            right_point = 263

            lx = int(face_landmarks.landmark[left_point].x * w)
            ly = int(face_landmarks.landmark[left_point].y * h)

            rx = int(face_landmarks.landmark[right_point].x * w)
            ry = int(face_landmarks.landmark[right_point].y * h)

            # Draw Eye Points
            cv2.circle(frame, (lx, ly), 5, (0, 255, 0), -1)
            cv2.circle(frame, (rx, ry), 5, (0, 255, 0), -1)

            # Detect Looking Away
            if abs(lx - rx) < 100:
                looking_away = True

    # Show Status
    if looking_away:

        cv2.putText(
            frame,
            "Looking Away Detected",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "Normal Behavior",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # Show Camera
    cv2.imshow(
        "Eye Tracking System",
        frame
    )

    # Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()