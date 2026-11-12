from __future__ import annotations

import base64
import os
from pathlib import Path
from threading import Lock
from typing import Any

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("PPE_MODEL_PATH", str(ROOT / "models" / "best.pt")))
FALLBACK_MODEL = os.getenv("YOLO_FALLBACK_MODEL", "yolov8n.pt")
CONFIDENCE = float(os.getenv("YOLO_CONFIDENCE", "0.35"))

app = FastAPI(title="AI Industrial Safety - Local YOLO", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

_model: YOLO | None = None
_model_lock = Lock()
_model_kind = "not-loaded"


class FramePayload(BaseModel):
    image: str = Field(..., description="Base64 JPEG data URL or base64 payload")


def get_model() -> YOLO:
    global _model, _model_kind
    if _model is None:
        with _model_lock:
            if _model is None:
                if MODEL_PATH.exists():
                    _model = YOLO(str(MODEL_PATH))
                    _model_kind = "custom-ppe"
                else:
                    _model = YOLO(FALLBACK_MODEL)
                    _model_kind = "general-person-demo"
    return _model


@app.get("/")
def home() -> FileResponse:
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/health")
def health() -> dict[str, Any]:
    custom_exists = MODEL_PATH.exists()
    return {
        "ok": True,
        "model_loaded": _model is not None,
        "model_mode": _model_kind,
        "custom_model_found": custom_exists,
        "message": (
            "Custom PPE model is available."
            if custom_exists
            else "No custom PPE model found. Fallback model is for general person-demo only."
        ),
    }


@app.post("/api/detect")
def detect(payload: FramePayload) -> dict[str, Any]:
    raw = payload.image.split(",", 1)[-1]
    try:
        decoded = base64.b64decode(raw, validate=True)
        image_array = np.frombuffer(decoded, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid image payload") from exc

    if frame is None:
        raise HTTPException(status_code=400, detail="Could not decode image")

    height, width = frame.shape[:2]
    if width > 960:
        scale = 960 / width
        frame = cv2.resize(frame, (960, int(height * scale)))

    try:
        model = get_model()
        result = model.predict(
            source=frame,
            device="cpu",
            conf=CONFIDENCE,
            imgsz=640,
            verbose=False,
        )[0]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {exc}") from exc

    names = result.names
    detections: list[dict[str, Any]] = []
    if result.boxes is not None:
        for box in result.boxes:
            cls_id = int(box.cls.item())
            confidence = float(box.conf.item())
            x1, y1, x2, y2 = [round(float(v), 1) for v in box.xyxy[0].tolist()]
            label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else names[cls_id]
            detections.append({
                "class_id": cls_id,
                "label": str(label),
                "confidence": round(confidence, 3),
                "box": [x1, y1, x2, y2],
            })

    return {
        "ok": True,
        "model_mode": _model_kind,
        "detections": detections,
        "image_width": int(frame.shape[1]),
        "image_height": int(frame.shape[0]),
        "warning": (
            "DEMO ONLY: general model results are not PPE compliance checks."
            if _model_kind != "custom-ppe"
            else "Prototype only: validate this PPE model before any operational safety use."
        ),
    }
