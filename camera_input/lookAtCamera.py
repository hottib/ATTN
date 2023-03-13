import cv2
import mediapipe as mp

# Load the Mediapipe face detection and pose estimation models
mp_face_detection = mp.solutions.face_detection
mp_pose = mp.solutions.pose

# Load the camera
cap = cv2.VideoCapture(0)

# Create a Mediapipe face detection and pose estimation objects
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection, \
        mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose_detection:
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the RGB image
        results = face_detection.process(frame_rgb)

        # Check if a face is detected in the image
        if results.detections:
            for detection in results.detections:
                # Get the bounding box coordinates of the face
                bbox = detection.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin * frame.shape[1]), int(bbox.ymin * frame.shape[0]), \
                             int(bbox.width * frame.shape[1]), int(bbox.height * frame.shape[0])

                # Draw a rectangle around the face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Crop the face region and convert it to RGB
                face_region = frame_rgb[y:y + h, x:x + w]
                face_region_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)

                # Detect facial landmarks and head pose in the face region
                pose_results = pose_detection.process(face_region_rgb)

                # Check if the person is looking at the camera
                if pose_results.pose_landmarks is not None:
                    left_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
                    right_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]
                    nose = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

                    # Calculate the average of the eye positions
                    eye_center = ((left_eye.x + right_eye.x) / 2, (left_eye.y + right_eye.y) / 2)

                    # Check if the nose is between the eyes and close to the camera
                    threshold = 0.5
                    if (eye_center[0] - threshold) < nose.x < (eye_center[0] + threshold )and \
                            eye_center[1] - threshold < nose.y < eye_center[1] + threshold:
                        # cv2.circle(image, center_coordinates, radius, color, thickness)
                        draw_eye_center = (int(eye_center[0]*height), int(eye_center[1]*width))
                        cv2.circle(frame, draw_eye_center, radius = 5, color= (0,255,255))
                        print(eye_center)
                        cv2.putText(frame, 'Looking at camera', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, 'Not looking at camera', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 0, 255), 2)
                else:
                    cv2.putText(frame, 'Cannot detect pose', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 0, 255), 2)
        cv2.imshow('Looking@Camera?', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()