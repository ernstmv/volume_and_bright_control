import mediapipe as mp
import cv2
import os

print("Version of mediapipe is ", mp.__version__)
print("Version of opencv is ", cv2.__version__)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

images_paht = "./hand_images"
image_name = "hand_two.jpg"
image_path1 = os.path.join(images_paht, image_name)

image = cv2.imread(image_path1)

with mp_hands.Hands(
        static_image_mode = True,
        max_num_hands = 2,
        min_tracking_confidence = 0.5,
        min_detection_confidence = 0.6) as hands:

#    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
#    print(results.multi_handedness)
    img_h, img_w, _ = image.shape
    for hand_landmarks in results.multi_hand_landmarks:
#        print("hand landmarks", hand_landmarks)
        finger_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * img_w
        finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * img_h
        print("Finger tip coordinate = ", (finger_tip_x, finger_tip_y))
        cv2.circle(image, (int(finger_tip_x), int(finger_tip_y)), radius = 6, thickness = 4, color=(255, 0, 0))

    mp_drawing.draw_landmarks(image,
            hand_landmarks, 
            mp_hands.HAND_CONNECTIONS, 
            mp_drawing_style.DrawingSpec(color=(255, 0, 255), thickness = 4))

    cv2.imshow("Hand 1 image: ", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
