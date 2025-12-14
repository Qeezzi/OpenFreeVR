# 🖐️ Unity Hand Tracking (MediaPipe + UDP)

Простой и быстрый способ перенести движения руки из веб-камеры в Unity.
Проект использует **Python (MediaPipe)** для отслеживания суставов и **UDP** для передачи координат в Unity без задержек.

---

## 📋 Что нужно

1. **Unity** (2022.3 или новее).
2. **Python** (3.8 – 3.11).
3. **Веб-камера**.

---

## ⚙️ Шаг 1: Настройка Python (Трекинг)

1. Откройте терминал (командную строку) и установите библиотеки:
   ```bash
   pip install mediapipe opencv-python
Создайте файл hand_tracker.py и вставьте в него этот код:
code
Python
import cv2
import mediapipe as mp
import socket
import struct

# Настройки
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
SHOW_WINDOW = True  # True = показывать окно с камерой

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

print(f"🚀 Трекинг запущен! Данные идут на {UDP_IP}:{UDP_PORT}")

while cap.isOpened():
    success, image = cap.read()
    if not success: continue

    # Обработка
    image = cv2.flip(image, 1)
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    points = [0.0] * 63
    detected = 0.0

    if results.multi_hand_landmarks:
        detected = 1.0
        lm = results.multi_hand_landmarks[0].landmark
        for i in range(21):
            # Конвертация координат для Unity
            points[i*3+0] = (lm[i].x - 0.5) * 2.0
            points[i*3+1] = -(lm[i].y - 0.5) * 2.0
            points[i*3+2] = -lm[i].z * 2.5

    # Отправка (64 float числа)
    data = struct.pack('64f', detected, *points)
    sock.sendto(data, (UDP_IP, UDP_PORT))

    if SHOW_WINDOW:
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Hand Tracker', image)
        if cv2.waitKey(1) & 0xFF == 27: break # ESC для выхода

cap.release()
cv2.destroyAllWindows()
🎮 Шаг 2: Настройка Unity
1. Подготовка сцены
Создайте пустой объект и назовите его HandRoot.
Создайте Куб (GameObject -> 3D Object -> Cube) и поставьте его перед камерой.
2. Создание скриптов
В папке Assets создайте папку Scripts и внутри неё два скрипта C#.
Скрипт A: CreateHandPoints.cs
(Нужен только для создания шариков-суставов)
code
C#
using UnityEngine;

public class CreateHandPoints : MonoBehaviour
{
    void Start()
    {
        for (int i = 0; i < 21; i++)
        {
            GameObject s = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            s.name = "Point" + i;
            s.transform.parent = transform;
            s.transform.localPosition = Vector3.zero;
            s.transform.localScale = Vector3.one * 0.03f;
            
            // Раскраска (по желанию)
            Renderer r = s.GetComponent<Renderer>();
            if (i == 0) r.material.color = Color.white;
            else if (i <= 4) r.material.color = Color.red;
            else if (i <= 8) r.material.color = Color.green;
            else r.material.color = Color.blue;
        }
        Destroy(this); // Удаляет сам скрипт после работы
    }
}
Скрипт B: HandUDPReceiver.cs
(Принимает данные и двигает руку)
code
C#
using UnityEngine;
using System.Net;
using System.Net.Sockets;

public class HandUDPReceiver : MonoBehaviour
{
    public Transform[] points; // Массив точек
    public GameObject cube;    // Куб для теста

    UdpClient client;

    void Start()
    {
        try {
            client = new UdpClient(5005);
            client.Client.ReceiveTimeout = 10;
        } catch {}
    }

    void Update()
    {
        if (client == null) return;
        try {
            IPEndPoint ep = null;
            byte[] data = client.Receive(ref ep);
            
            if (data.Length != 256) return; // Проверка размера пакета

            float detected = System.BitConverter.ToSingle(data, 0);
            if (detected < 0.5f) return; // Руки нет

            for (int i = 0; i < 21; i++)
            {
                int offset = 4 + i * 12;
                float x = System.BitConverter.ToSingle(data, offset + 0);
                float y = System.BitConverter.ToSingle(data, offset + 4);
                float z = System.BitConverter.ToSingle(data, offset + 8);
                
                if(points[i] != null)
                    points[i].position = new Vector3(x, y, 1.5f + z);
            }

            // Проверка касания куба (указательным пальцем - точка 8)
            if (cube != null && points[8] != null)
            {
                float dist = Vector3.Distance(points[8].position, cube.transform.position);
                cube.GetComponent<Renderer>().material.color = dist < 0.15f ? Color.green : Color.white;
            }
        } catch {}
    }

    void OnDestroy() => client?.Close();
}
🔗 Шаг 3: Сборка (Самый важный момент!)
Киньте скрипт CreateHandPoints на объект HandRoot.
Нажмите Play ▶️.
В HandRoot появятся точки Point0...Point20.
Не выключая Play: Выделите все точки (Shift+Click), нажмите Ctrl+C (копировать).
Нажмите Stop ⏹️ (точки исчезнут).
Нажмите Ctrl+V (вставить) — точки вернутся и станут постоянными.
Удалите компонент CreateHandPoints с HandRoot.
Киньте скрипт HandUDPReceiver на HandRoot.
В поле Points (Size = 21) перетащите ваши точки:
Point0 → Element 0
...
Point20 → Element 20
Перетащите Куб в поле Cube.
🚀 Запуск
Запустите Python: python hand_tracker.py
Запустите Unity: нажмите Play.
Покажите руку в камеру — скелет в Unity оживет!
Коснитесь виртуального куба указательным пальцем — он станет зеленым.
