# Glove Hand Tracker and Unity Receiver

This repository contains a Python-based hand tracking sender and a Unity receiver that visualizes/uses tracked hand points. The Python script detects hand landmarks and streams them (typically via UDP) to Unity.

## Repository Structure

- `python/`
  - `hand_tracker_fast.py` — optimized Python sender that tracks hands and streams data.
  - `requirements.txt` — Python dependencies for the tracker.
- `hand_tracker.py` — alternative/legacy Python sender at the repo root.
- `unity/`
  - `Assets/Scripts/CreateHandPoints.cs` — creates point objects in the Unity scene.
  - `Assets/Scripts/HandUDPReceiver.cs` — receives streamed data (e.g., via UDP) and updates points.
  - `README-Unity.md` — Unity-specific notes.
- `.gitignore`

If something in your local copy differs, follow the paths present in your workspace.

## Prerequisites

- Python 3.9+ (Windows, macOS, or Linux)
- pip (or pipx) to install dependencies
- A working webcam (for live tracking) or a video file
- Unity 2021.3+ (LTS recommended)

## Python Setup

1. Create a virtual environment (recommended):
   - Windows:
     - `python -m venv .venv`
     - `.venv\\Scripts\\activate`
   - macOS/Linux:
     - `python3 -m venv .venv`
     - `source .venv/bin/activate`

2. Install dependencies:
   - If using the repo-root `requirements.txt` inside `python/`:
     - `pip install -r python/requirements.txt`
   - If you use the top-level `requirements.txt` (present at repo root):
     - `pip install -r requirements.txt`

3. Verify OpenCV GUI support (for preview windows) if you need visualization.

## Running the Python Sender

Choose one of the available scripts.

- Faster sender in `python/` directory:
  - `python python/hand_tracker_fast.py`

- Alternate sender at repository root:
  - `python hand_tracker.py`

Common options typically include:
- Input source selection (webcam index like `--camera 0` or video path `--video file.mp4`).
- Network settings (target IP/port) for Unity receiver.

Open the file you intend to run and review the top-level constants or argparse flags for the exact parameters supported. If no flags are present, edit the constants in the script to match your environment (e.g., `UDP_IP`, `UDP_PORT`, camera index).

## Unity Setup

1. Open the `unity/` folder as a Unity project or copy the `Assets` into your Unity project.
2. Ensure the scene contains an empty GameObject with the `HandUDPReceiver` component attached.
3. Optionally add `CreateHandPoints` to auto-generate GameObjects for each landmark index.
4. Match the network settings with the Python sender (same port; IP should be localhost or your machine IP if running across devices).
5. Enter Play Mode. You should see points update when the Python sender is running.

See `unity/README-Unity.md` for additional Unity-specific instructions and any scene setup details.

## Data Format

The exact payload may differ between scripts, but commonly:
- A single UDP datagram per frame.
- Contains normalized or pixel coordinates for each hand landmark.
- Often comma- or space-separated values, sometimes prefixed with hand id or count.

Inspect the Python sender to confirm the schema and adjust the Unity receiver parsing if needed.

## Troubleshooting

- No data in Unity:
  - Confirm Python script is running without errors.
  - Verify sender and receiver share the same port and network interface.
  - Disable firewall for the chosen UDP port or add an allow rule.
  - If using Wi-Fi, ensure both devices are on the same subnet.
- Camera not found:
  - Try `--camera 0`, `--camera 1`, etc.
  - Close other apps using the camera.
- Preview window not showing:
  - Your OpenCV build might lack GUI support; run headless and rely on Unity visualization.
- Performance issues:
  - Use `hand_tracker_fast.py`.
  - Reduce frame size or FPS.
  - Limit to a single hand if your use-case allows.

## Development Notes

- Keep Python and Unity data structures in sync (landmark count and ordering).
- Consider time-stamping frames to help with latency diagnostics.
- Add basic message versioning in the payload to avoid silent mismatches.

## License

Specify your license here (e.g., MIT). If none is provided, all rights reserved.

## Acknowledgements

- OpenCV and MediaPipe (if used in your Python scripts)
- Unity
