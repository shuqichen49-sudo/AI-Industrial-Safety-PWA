# AI Industrial Safety — CES 2028 Release Candidate (development prototype)

## What is included
- Responsive Chinese / English / Korean web dashboard.
- Demo monitoring mode with simulated person/PPE/face overlays.
- Optional local webcam preview. Opening the webcam does **not** run inference.
- Explicitly labelled sample vital signs.
- Internal front-end QA checks and a local Edge API connection test.
- FastAPI Edge demo endpoint for validating and recording incoming vital-data payloads.
- Unit tests for API health, missing data, timestamp timezone and blood-pressure semantic validation.
- CES 2028 readiness checklist.

## Run the website
From this directory:
```bash
python -m http.server 8000
```
Open `http://127.0.0.1:8000`.

## Run the local Edge API
Use Python 3.10+:
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn edge_server:app --host 127.0.0.1 --port 8765
```
Keep the Edge API terminal running. On the website, click **Check Edge connection** and then **Send demo data to Edge**. A successful HTTP response means the demo payload was accepted by this local development API—not that a smartwatch was connected.

## Run API tests
```bash
pip install -r requirements.txt
pip install httpx
python -m unittest -v test_edge_server.py
```
The tests are supplied but have not been run in the user's target environment. Re-run them after installing dependencies.

## Important: current limits
- No real YOLO weights or inference runtime are bundled.
- No real MediaPipe inference is bundled. Face boxes in demo mode are simulated.
- The camera mode only displays camera preview; it does not perform AI detection.
- No actual smartwatch is connected. The payload sent to the Edge API is explicitly simulated.
- The Edge API is unauthenticated and for local development only. It binds to loopback by default; do not expose it to a LAN or the public internet.
- JSONL storage is demonstration storage, not a production medical-data store.
- This prototype is not a medical device, not a certified industrial safety system, and not ready for safety-critical deployment.

## Recommended release engineering
1. Freeze hardware/software bill of materials and target operating environment.
2. Select exact camera, edge computer, watch model, firmware, and documented vendor SDK/API.
3. Implement real YOLO detection + tracking and MediaPipe face detection, with version-pinned models and privacy controls.
4. Implement device-authorized wearable integration; preserve source, timestamps, units, calibration/quality, and skin-vs-core temperature distinctions.
5. Build a labelled test set and evaluate precision, recall, false positives, false negatives, latency and frame drops by lighting/occlusion/worker count.
6. Run fault injection: camera disconnect, Edge reboot, network loss, duplicate/stale/out-of-order data, storage full and clock drift.
7. Add authentication, TLS, least-privilege access, encrypted storage, retention/deletion policy, audit logs and incident response.
8. Validate on target factory hardware and in the intended environment; obtain relevant safety, privacy, radio and medical regulatory advice where applicable.
9. Keep a traceable release report: test ID, version, environment, expected result, actual result, evidence, defect and sign-off.

## Safety and privacy
Face detection is configured as detection-only; do not add identity recognition or biometric retention without a documented lawful basis, privacy impact assessment and appropriate controls. Do not use demo vital values for health decisions. Smartwatch blood-pressure and temperature capabilities vary by model; skin temperature is not core body temperature. Missing or unsupported measurements must remain missing rather than being fabricated.
