# Local YOLO webcam test (Windows CPU)

This folder runs a local FastAPI + Ultralytics YOLO prototype. It is intentionally separate from the public Vercel PWA: webcam frames are processed on this Windows computer and are not sent to Vercel.

## Requirements

- Windows 10/11, 64-bit
- Python 3.11 (64-bit)
- A webcam
- Internet for the first dependency/model download

## Start

1. Download or clone this repository.
2. Open the `local-yolo` folder.
3. Double-click `start_windows.bat`.
4. Wait for dependencies to install on first launch.
5. Open http://127.0.0.1:8000 if the browser does not open automatically.
6. Allow camera access in the browser.

The first launch downloads the small `yolov8n.pt` fallback model. CPU inference may be slow.

## Important model distinction

- If `models/best.pt` is absent, the app uses the generic COCO `yolov8n.pt` model. This is only a general object/person demonstration and is **not** a hard-hat or reflective-vest compliance detector.
- To enable PPE-specific labels, place a validated Ultralytics-compatible PPE model at `models/best.pt`. The model's class names are displayed as returned by that model.
- Do not assume a model is reliable just because it draws boxes. Validate it on representative workplace footage, including lighting, distance, occlusion, camera angle, and different PPE types.

You can change the model path with `PPE_MODEL_PATH` and confidence with `YOLO_CONFIDENCE` environment variables.

## API

- `GET /api/health` — local runtime/model status
- `POST /api/detect` — accepts JSON `{"image":"data:image/jpeg;base64,..."}` and returns detections

The API binds to `127.0.0.1` only. Do not expose it directly to the public internet.

## Safety and privacy

This is a development prototype, not a certified safety system. It must not be used as the sole basis for alarms, disciplinary action, access control, or emergency decisions. Keep a human safety officer in the loop. Camera access stays in the local browser and frame inference is performed by the local Python process.
