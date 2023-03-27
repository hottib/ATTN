import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# empirical absolute value of centered centering_vertical_raw
centering_vertical_middle = 8
# maximum absolute value of centering_vertical
centering_vertical_limit = 3

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    mouth_left= results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
    mouth_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]
    ear_left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
    ear_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
    nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

    mouth_length = (mouth_right.x - mouth_left.x)**2 +(mouth_right.y - mouth_left.y)**2

    # calculate the slope of the line between the ears
    slope = (ear_right.y - ear_left.y)/(ear_right.x - ear_left.x)
    # calculate the y-intercept of the line between the ears
    intercept_y = ear_left.y - slope*ear_left.x

    # calculate the projection of the nose onto the line between the ears
    nose_projection = np.array([nose.x, slope*nose.x + intercept_y])

    # calculate how centered the nose_projection is on the line between the ears
    centering_horizontal = (nose_projection[0] - (ear_left.x + ear_right.x)/2)/(ear_right.x - ear_left.x)

    # calculate how centered the nose is on the line between the ears
    # centering_horizontal_nose = (nose.x - (ear_left.x + ear_right.x)/2)/(ear_right.x - ear_left.x)

    # absolute value of centering_horizontal
    centering_horizontal = abs(centering_horizontal)

    # calculate y distance between nose and nose_projection as a fraction of mouth_length
    centering_vertical_raw = (nose.y - nose_projection[1])/mouth_length

    # normlize centering_vertical_raw (-1 to 1 where 0 is centered)
    centering_vertical_relative = (centering_vertical_raw - centering_vertical_middle)/centering_vertical_middle

    # limit centering_vertical_relative to -1 to 1
    centering_vertical = max(min(centering_vertical_relative, centering_vertical_limit), -centering_vertical_limit)/centering_vertical_limit

    # combine centering_horizontal and centering_vertical into one measure, using pythagorean theorem
    centering = (centering_horizontal**2 + centering_vertical**2)**0.5
    
    try: 
        print(centering_horizontal, centering_vertical)
    except:
        ...
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #draw an overlay on the image
    # green when centered
    # red when not centered
    # gradually
    # from green to red
    # as centering_horizontal increases
    # from 0 to 1
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (image.shape[1], image.shape[0]), (0, 255*centering, 255*(1-centering)), -1)
    cv2.addWeighted(overlay, 1-centering, image, (centering), 0, image)

    # draw nose_projection
    cv2.circle(image, (int(nose_projection[0]*image.shape[1]), int(nose_projection[1]*image.shape[0])), 5, (0, 0, 255), -1)
    
    # draw nose
    cv2.circle(image, (int(nose.x*image.shape[1]), int(nose.y*image.shape[0])), 5, (0, 255, 0), -1)
    # draw line between ears
    cv2.line(image, (int(ear_left.x*image.shape[1]), int(ear_left.y*image.shape[0])), (int(ear_right.x*image.shape[1]), int(ear_right.y*image.shape[0])), (255, 0, 0), 2)
    # draw line between nose and nose_projection
    #cv2.line(image, (int(nose.x*image.shape[1]), int(nose.y*image.shape[0])), (int(nose_projection[0]*image.shape[1]), int(nose_projection[1]*image.shape[0])), (255, 0, 0), 2)

    """
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    """

    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
