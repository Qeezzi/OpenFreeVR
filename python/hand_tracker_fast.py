# hand_tracker_fast.py
import cv2
import mediapipe as mp
import socket
import struct
import time

SHOW_PREVIEW = True
UDP_IP = "127.0.0.1"  # если Unity на другом ПК, укажите его IP
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.4,
    min_tracking_confidence=0.4,
    model_complexity=0
)

cap = cv2.VideoCapture(0)
print("🚀 Запущен трекинг рук. ESC — выход.")

frame_count = 0
start = time.perf_counter()

while cap.isOpened():
    ok, image = cap.read()
    if not ok:
        continue

    image = cv2.flip(image, 1)
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    points = [0.0] * 63
    detected = 0.0

    if results.multi_hand_landmarks:
        detected = 1.0
        lm = results.multi_hand_landmarks[0].landmark
        for i in range(21):
            points[i*3+0] = (lm[i].x - 0.5) * 2.0
            points[i*3+1] = -(lm[i].y - 0.5) * 2.0
            points[i*3+2] = -lm[i].z * 2.5

    data = struct.pack('64f', detected, *points)
    sock.sendto(data, (UDP_IP, UDP_PORT))

    if SHOW_PREVIEW:
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Hand Tracker (ESC to quit)', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    frame_count += 1
    if frame_count % 30 == 0:
        now = time.perf_counter()
        fps = 30.0 / (now - start)
        print(f"FPS≈{fps:.0f} | Hand={'✅' if detected else '❌'}")
        start = now

cap.release()
cv2.destroyAllWindows()
