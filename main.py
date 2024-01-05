import os
import sys
import subprocess
from math import sqrt
import cv2
import mediapipe as mp

WIN_NAME = "Camera"
N_HANDS = 2

mp_drw = mp.solutions.drawing_utils
mp_drw_stl = mp.solutions.drawing_styles
mp_hnds = mp.solutions.hands
hands = mp_hnds.Hands(max_num_hands = N_HANDS)


def set_bright(brightness):

    backlight_dir = r'/sys/class/backlight/intel_backlight'
    brightness_file_path = os.path.join(backlight_dir, 'brightness')

    with open(brightness_file_path, 'w') as file:
        file.write(str(brightness))
    

def set_volume(volume):
    subprocess.run(['amixer', 'set', 'Master', f'{volume}%'])


def set_parameter(ref_dist, dist, parameter, frame, idx_tip_x, idx_tip_y, thmb_tip_x, thmb_tip_y):
    
    max_v = 100 if parameter else 96000
    min_v = 1 if parameter else 9600
    val = dist * (max_v / ref_dist)

    if val > max_v: val = max_v
    if val < 0: val = min_v

    label = f"Volume: {round(val, 1)}" if parameter else f"Bright: {round(val, 1)}"
    pos = (10, 470) if parameter else (10, 450)
    color = (0, 255, 0) if parameter else (255, 255, 0)

    if parameter: set_volume(val)
    else: set_bright(int(val))

    cv2.putText(frame, label, pos, 2, 0.5, color)
    cv2.line(frame, (int(idx_tip_x), int(idx_tip_y)), (int(thmb_tip_x), int(thmb_tip_y)), color, 1)


def main():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)

    s = 0
    if len(sys.argv) > 1: s = sys.argv[1]
    source = cv2.VideoCapture(s)

    while source.isOpened():
        has_frame, frame = source.read()
        parameter = True
        if not has_frame: break
        frame = cv2.flip(frame, 1)
        img_h, img_w, _ = frame.shape
        results = hands.process(frame)
        for i in range(N_HANDS):
            try:
                hnd_lndmrks = results.multi_hand_landmarks[-(i+1)]
                mp_drw.draw_landmarks(frame, hnd_lndmrks, mp_hnds.HAND_CONNECTIONS)

                idx_tip_x = hnd_lndmrks.landmark[mp_hnds.HandLandmark.INDEX_FINGER_TIP].x * img_w
                idx_tip_y = hnd_lndmrks.landmark[mp_hnds.HandLandmark.INDEX_FINGER_TIP].y * img_h

                thmb_tip_x = hnd_lndmrks.landmark[mp_hnds.HandLandmark.THUMB_TIP].x * img_w
                thmb_tip_y = hnd_lndmrks.landmark[mp_hnds.HandLandmark.THUMB_TIP].y * img_h

                dist = sqrt((idx_tip_x - thmb_tip_x) ** 2 + (idx_tip_y - thmb_tip_y) ** 2)

                wrist_x = hnd_lndmrks.landmark[mp_hnds.HandLandmark.WRIST].x * img_w
                wrist_y = hnd_lndmrks.landmark[mp_hnds.HandLandmark.WRIST].y * img_h

                idx_base_x = hnd_lndmrks.landmark[mp_hnds.HandLandmark.INDEX_FINGER_MCP].x * img_w
                idx_base_y = hnd_lndmrks.landmark[mp_hnds.HandLandmark.INDEX_FINGER_MCP].y * img_h

                ref_dist = sqrt((idx_base_x - wrist_x) ** 2 + (idx_base_y - wrist_y) ** 2) * 1.5

                set_parameter(ref_dist, dist, parameter, frame, idx_tip_x, idx_tip_y, thmb_tip_x, thmb_tip_y)
                
                parameter = not parameter

            except Exception: pass
        cv2.imshow(WIN_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    source.release()
    cv2.destroyWindow(WIN_NAME)


if __name__ == "__main__":
    main()
