# Инструкция по Unity (минимальный прототип)

Версия Unity: 2022.3 LTS (Built-in Render Pipeline)

## Шаги
1. Откройте проект `unity/` в Unity.
2. Создайте сцену `Assets/Scenes/HandScene.unity` (если не существует).
3. В сцене:
   - Добавьте пустой объект `HandRoot`.
   - На `HandRoot` повесьте компоненты: `CreateHandPoints` и `HandUDPReceiver`.
   - Нажмите Play → появятся `Point0..Point20`. Остановите Play.
   - Создайте пустой объект `HandPoints` и переместите его под `HandRoot`.
   - Запустите Play снова, выделите все `Point0..Point20` → Ctrl+C, остановите Play → выберите `HandPoints` → Ctrl+V. 
   - Удалите компонент `CreateHandPoints` с `HandRoot` (теперь точки постоянные).
   - В `HandUDPReceiver` установите `Points` → Size = 21 и перетащите `HandPoints/Point0..Point20` по индексам 0..20.
   - Создайте `Cube` и перетащите его в поле `cube` компонента `HandUDPReceiver`.
4. Сохраните сцену.
5. Запустите Python (в корне репозитория):
   ```bash
   pip install -r python/requirements.txt
   python python/hand_tracker_fast.py
   ```
6. В Unity нажмите Play — точки руки двигаются, при приближении `Point8` к кубу куб зеленеет.

## Примечания
- UDP порт: 5005 (локальная машина). Если Python на другом ПК, поменяйте IP в `hand_tracker_fast.py`.
- Масштаб/смещение можно править в `HandUDPReceiver` (смещение 1.5f по Z).
- Для второй руки потребуется расширить протокол и добавить второй набор точек/порт.
