import cv2
import mediapipe as mp

# Load the Mediapipe face detection model
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

# Load the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to RGB and pass it through the face detection model
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)

    # Draw the bounding boxes on the frame
    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            x = int(bbox.xmin * frame.shape[1])
            y = int(bbox.ymin * frame.shape[0])
            w = int(bbox.width * frame.shape[1])
            h = int(bbox.height * frame.shape[0])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the windowimport cv2
import mediapipe as mp

# Load the Mediapipe face mesh model
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Load the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to RGB and pass it through the face mesh model
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    # Draw the landmarks on the frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for i, landmark in enumerate(face_landmarks.landmark):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), radius=1, color=(0, 0, 255), thickness=-1)

    # Display the frame
    cv2.imshow('Face Mesh', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

cap.release()
cv2.destroyAllWindows()
