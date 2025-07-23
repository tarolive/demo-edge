from pathlib import Path
from uuid import uuid4
from dotenv import load_dotenv
from ultralytics import YOLO
import os

ROOT = Path(__file__).resolve().parent
load_dotenv(override=False)                 # don't overwrite real ENV vars

EDGE_ID     : str = os.getenv("EDGE_ID") or str(uuid4())
EDGE_SERVER : str = os.environ["EDGE_SERVER"]        # raise if missing
URL_CAMERA  : str = os.getenv("URL_CAMERA", "0")
CAMERA_ID   : str = os.getenv("CAMERA_ID") or str(uuid4())

MODEL_PATH  : str   = os.getenv(
    "MODEL_PATH",
    str(ROOT.parent / "weights" / "yolov8s.pt")
)
CONF        : float = float(os.getenv("CONF", "0.25"))
IMG_SIZE    : int   = int(os.getenv("IMG_SIZE", "416"))

model = YOLO(MODEL_PATH)


def as_dict() -> dict:
    """Return all runtime-relevant settings as a dictionary (for logging)."""
    return {
        "EDGE_ID": EDGE_ID,
        "EDGE_SERVER": EDGE_SERVER,
        "URL_CAMERA": URL_CAMERA,
        "CAMERA_ID": CAMERA_ID,
        "MODEL_PATH": MODEL_PATH,
        "CONF": CONF,
        "IMG_SIZE": IMG_SIZE,
    }
