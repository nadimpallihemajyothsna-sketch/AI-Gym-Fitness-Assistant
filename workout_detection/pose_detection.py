import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process pose
    results = pose.process(rgb_frame)

    # Draw landmarks
    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # Show webcam
    cv2.imshow("AI Workout Detection", frame)

    # Press ESC to close
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()