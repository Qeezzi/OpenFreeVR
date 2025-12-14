# OpenFreeVR
Система VR-взаимодействия с трекингом рук: веб-камера ПК отслеживает 21 точку руки через MediaPipe, данные передаются в Unity. Телефон работает как VR-шлем, используя AR Foundation для определения положения в пространстве по окружению.
# VR Hand Tracking → Unity (без перчатки)

Репозиторий с минимальным прототипом: камера ПК отслеживает руку (MediaPipe), координаты 21 точек передаются в Unity по UDP, где отображается скелет руки и простой интерактив (куб зеленеет при касании).

— Подходит для дальнейшей интеграции с телефоном как VR‑шлемом (ALVR/Virtual Desktop) и AR‑позиционированием головы.

## Возможности
- Отслеживание одной руки через MediaPipe (21 landmark)
- UDP‑мост: Python → Unity (порт 5005)
- Минимальная сцена Unity: 21 сферическая точка + куб (индикация касания)
- Готово для расширения: AR‑поза шлема, SteamVR/OpenXR, две руки

## Структура
```
README.md
LICENSE                # будет добавлена (MIT по умолчанию)
.gitignore             # будет добавлен (Python + Unity)

python/
  hand_tracker_fast.py # трекинг MediaPipe + UDP
  requirements.txt     # зависимости Python

unity/
  Assets/
    Scenes/HandScene.unity        # сцена (создадите в Unity, инструкции ниже)
    Scripts/
      HandUDPReceiver.cs          # приём координат в Unity
      CreateHandPoints.cs         # разовое создание 21 точки
    README-Unity.md               # пошаговый запуск в Unity

.github/
  ISSUE_TEMPLATE/
    bug_report.md       # шаблон бага
    feature_request.md  # запрос фичи

docs/
  images/
  demo.gif              # демо (добавите позже)
```

## Быстрый запуск

### 1) Python (Windows)
1. Установите Python 3.10–3.11 (64-bit) с добавлением в PATH.
2. Установите зависимости:
   ```bash
   pip install -r python/requirements.txt
   ```
3. Запустите трекинг:
   ```bash
   python python/hand_tracker_fast.py
   ```
   Откроется окно с камерой и костями. В консоль печатается FPS.

### 2) Unity (2022.3 LTS)
1. Откройте папку `unity/` как проект Unity (или создайте новый и добавьте содержимое).
2. Создайте сцену `Assets/Scenes/HandScene.unity` (если не существует) и добавьте:
   - Пустой объект `HandRoot`.
   - Скрипты из `Assets/Scripts`: `CreateHandPoints.cs` и `HandUDPReceiver.cs`.
   - Нажмите Play → появятся `Point0..Point20` → скопируйте их в постоянный контейнер `HandPoints` (см. `README-Unity.md`).
   - В `HandUDPReceiver` заполните массив `Points` ссылками на 21 точку, задайте `Cube`.
3. Нажмите Play. При запущенном Python сферы будут двигаться, куб зеленеет при касании указательным пальцем (Point8).

Подробная инструкция — в `unity/Assets/README-Unity.md`.

## Настройка портов/брандмауэра
- По умолчанию используется UDP порт 5005 (localhost → Unity на той же машине).
- Если Unity и Python на разных устройствах — укажите IP Unity‑машины в `hand_tracker_fast.py` и разрешите UDP в брандмауэре.

## Roadmap
- [ ] Вторая рука (две руки в Python и в Unity)
- [ ] Сглаживание/фильтрация (экспоненциальный/Калман)
- [ ] Передача AR‑позиции шлема с телефона (порт 5006) и привязка к камере в Unity
- [ ] Интеграция со SteamVR/OpenXR (ALVR/Virtual Desktop)
- [ ] Готовый пакет сцены и префабы руки

## FAQ
- «Не вижу окно камеры»: проверьте, что `SHOW_PREVIEW = True` в `hand_tracker_fast.py`.
- «Сферы не двигаются»: убедитесь, что Python запущен, порт 5005 не заблокирован, в инспекторе `Points` заполнены 21 ссылкой.
- «Точки исчезают после Stop»: используйте `CreateHandPoints` только для генерации, затем скопируйте точки в постоянный объект `HandPoints` и удалите компонент `CreateHandPoints`.

## Благодарности
- Google MediaPipe
- Unity
