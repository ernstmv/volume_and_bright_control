import sys
import cv2
import mediapipe as mp

def accesing_cam():
    s=0
    if len(sys.argv) > 1: s = sys.argv[1]
    return cv2.VideoCapture(s)

def main():
    win_name = "Camera"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    source=accesing_cam()
    mp_drw =  mp.solutions.drawing_utils
    mp_drw_stl = mp.solutions.drawing_styles
    mp_hnds = mp.solutions.hands

    while cv2.waitKey(1) != 27:
        has_frame, frame = source.read()
        if not has_frame: break
        frame = cv2.flip(frame, 1)

        with mp_hnds.Hands(
                static_image_mode = True,
                max_num_hands = 2,
                min_tracking_confidence = 0.5,
                min_detection_confidence = 0.6) as hands:
            results=hands.process(frame)
            try:
                mp_drw.draw_landmarks(
                        frame, 
                        results.multi_hand_landmarks[-1],
                        mp_hnds.HAND_CONNECTIONS, 
                        mp_drw_stl.DrawingSpec(color = (255,0, 255), thickness = 4))
            except Exception: pass
        cv2.imshow(win_name, frame)

    source.release()
    cv2.destroyWindow(win_name)

if __name__ == "__main__":
    main()
