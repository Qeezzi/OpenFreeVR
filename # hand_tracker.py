# hand_tracker_fast.py
import cv2
import mediapipe as mp
import socket
import struct
import time

# ⚙️ НАСТРОЙКИ
SHOW_PREVIEW = True        # True — показывать окно, False — только в Unity
USE_FLIP = True           # True — зеркальное отображение (как в зеркале), False — как есть

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# 🔌 Инициализация
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.4,
    min_tracking_confidence=0.4,
    model_complexity=0  # 0 = быстрая
)

# 📸 Захват — стандартный, без CAP_DSHOW (если у тебя проблемы с ним)
cap = cv2.VideoCapture(0)  # ← БЕЗ cv2.CAP_DSHOW — это "как было"

# ⚠️ Если камера не открывается — попробуй:
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # раскомментируй эту строку и закомментируй предыдущую

print(f"🎥 Камера: стандартная | Зеркало: {'ВКЛ' if USE_FLIP else 'ВЫКЛ'} | Preview: {'ВКЛ' if SHOW_PREVIEW else 'ВЫКЛ'}")

frame_count = 0
start_time = time.perf_counter()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # 🔄 Зеркалирование (optional)
    if USE_FLIP:
        image = cv2.flip(image, 1)  # 1 = горизонтальное (зеркало), 0 = вертикальное

    # 📐 Отправляем в MediaPipe в RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # 📍 Подготовка данных
    points = [0.0] * 63
    hand_detected = 0.0

    if results.multi_hand_landmarks:
        hand_detected = 1.0
        lm = results.multi_hand_landmarks[0].landmark
        for i in range(21):
            # Отправляем координаты так, как они есть в MediaPipe (но центрируем)
            x = (lm[i].x - 0.5) * 2.0   # → [-1, 1]
            y = -(lm[i].y - 0.5) * 2.0  # инвертируем Y (в Unity Y↑, в MediaPipe Y↓)
            z = -lm[i].z * 2.5
            points[i*3 + 0] = x
            points[i*3 + 1] = y
            points[i*3 + 2] = z

    # 📤 Отправка в Unity
    data = struct.pack('64f', hand_detected, *points)
    sock.sendto(data, (UDP_IP, UDP_PORT))

    # 👁️ Визуализация (если нужно)
    if SHOW_PREVIEW:
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(0, 150, 255), thickness=2)
                )
        cv2.imshow('Hand Tracker (ESC to quit)', image)
        if cv2.waitKey(5) & 0xFF == 27:  # ESC
            break

    # 📊 FPS
    frame_count += 1
    if frame_count % 30 == 0:
        fps = frame_count / (time.perf_counter() - start_time)
        print(f"⚡ FPS: {fps:.0f} | Hand: {'✅' if hand_detected else '❌'}")
        frame_count = 0
        start_time = time.perf_counter()

cap.release()
cv2.destroyAllWindows()