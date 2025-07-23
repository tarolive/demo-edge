import cv2, time, base64
import numpy as np
from typing import Tuple, List, Dict, Any

from src import config

_model   = config.model
CONF     = config.CONF
IMG_SIZE = config.IMG_SIZE


def _encode_image_b64(img: np.ndarray) -> str:
    """Convert an OpenCV BGR image → JPG → base64 (ASCII str)."""
    ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    if not ok:
        raise RuntimeError("Failed to encode frame as JPG")
    return base64.b64encode(buf.tobytes()).decode("ascii")


def run_inference(frame: np.ndarray) -> Tuple[Dict[str, Any], np.ndarray]:
    """
    Returns:
        payload .. JSON-serialisable dict with metadata
        annotated .. BGR image with boxes
    """
    t0 = time.time()
    results = _model.predict(frame, imgsz=IMG_SIZE, conf=CONF,
                             device="cpu", verbose=False)[0]

    # build label list
    labels: List[str] = [ _model.names[int(i)] for i in results.boxes.cls ]

    annotated = results.plot()

    payload = {
        "edge_id":   config.EDGE_ID,
        "camera_id": config.CAMERA_ID,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(t0)),
        "labels":    labels,
        "img_width":  annotated.shape[1],
        "img_height": annotated.shape[0],
        # Optional: omit bbox list to save bandwidth
    }

    if labels:
        payload["annotated_jpg_base64"] = _encode_image_b64(annotated)

    return payload, annotated
