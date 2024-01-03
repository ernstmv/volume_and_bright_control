import sys
import cv2
import mediapipe as mp

WIN_NAME = "Camera"
N_HANDS = 2

mp_drw =  mp.solutions.drawing_utils
mp_drw_stl = mp.solutions.drawing_styles
mp_hnds = mp.solutions.hands
hands=mp_hnds.Hands(max_num_hands = N_HANDS)

def main():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)

    s=0
    if len(sys.argv) > 1: s = sys.argv[1]
    source=cv2.VideoCapture(s)

    while source.isOpened():
        has_frame, frame = source.read()
        if not has_frame: break
        frame=cv2.flip(frame, 1)
        results = hands.process(frame)
        for i in range(N_HANDS):
            try:
                mp_drw.draw_landmarks(frame, results.multi_hand_landmarks[-(i+1)], mp_hnds.HAND_CONNECTIONS)
            except Exception: pass
        cv2.imshow(WIN_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break
    source.release()
    cv2.destroyWindow(WIN_NAME)

if __name__ == "__main__":
    main()
