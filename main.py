import sys
import subprocess
from math import sqrt
import cv2
import mediapipe as mp

WIN_NAME = "Camera"
N_HANDS = 1

mp_drw =  mp.solutions.drawing_utils
mp_drw_stl = mp.solutions.drawing_styles
mp_hnds = mp.solutions.hands
hands=mp_hnds.Hands(max_num_hands = N_HANDS)

def set_volume(volume):
    try:
        subprocess.run(['amixer', 'set', 'Master', f'{volume}%'])
    except Exception as e:
        print(f"Error al establecer el volumen: {e}")

def main():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)

    s=0
    if len(sys.argv) > 1: s = sys.argv[1]
    source=cv2.VideoCapture(s)

    while source.isOpened():
        has_frame, frame = source.read()
        if not has_frame: break
        frame=cv2.flip(frame, 1)
        img_h, img_w, _ = frame.shape
        results = hands.process(frame)
        for i in range(N_HANDS):
            try:
                hnd_lndmrks =  results.multi_hand_landmarks[-(i+1)]
                mp_drw.draw_landmarks(frame, hnd_lndmrks, mp_hnds.HAND_CONNECTIONS)

                idx_tip_x = hnd_lndmrks.landmark[mp_hnds.HandLandmark.INDEX_FINGER_TIP].x * img_w
                idx_tip_y = hnd_lndmrks.landmark[mp_hnds.HandLandmark.INDEX_FINGER_TIP].y * img_h

                thmb_tip_x = hnd_lndmrks.landmark[mp_hnds.HandLandmark.THUMB_TIP].x * img_w
                thmb_tip_y = hnd_lndmrks.landmark[mp_hnds.HandLandmark.THUMB_TIP].y * img_h
                
                dist = sqrt((idx_tip_x - thmb_tip_x) ** 2 + (idx_tip_y - thmb_tip_y) ** 2)

                vol = dist * (100 / 260)
                if vol > 100: vol = 100
                if vol < 0: vol = 0

                set_volume(vol)
                cv2.line(frame, (int(idx_tip_x), int(idx_tip_y)), (int(thmb_tip_x), int(thmb_tip_y)), (255, 0, 0), 5)

            except Exception: pass
        cv2.imshow(WIN_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break
    source.release()
    cv2.destroyWindow(WIN_NAME)

if __name__ == "__main__":
    main()
