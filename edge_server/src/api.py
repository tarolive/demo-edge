from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from src import store

class Detection(BaseModel):
    edge_id: str
    camera_id: str
    timestamp: str
    labels: List[str]
    img_width: int
    img_height: int
    annotated_jpg_base64: Optional[str] = Field(None, description="Base64 JPG")

app = FastAPI(title="Edge-Server Inference Receiver")


@app.post("/inference", status_code=204)
async def receive_inference(det: Detection):
    """Receive detections from clients – store in RAM."""
    if not det.labels:
        # ignoring empty detections keeps dashboard clean, but configurable
        raise HTTPException(status_code=400, detail="No labels supplied")

    await store.add(det.edge_id, det.dict())
    return None  # 204 No Content

@app.get("/objects/{edge_id}/{camera_id}", response_model=List[str])
async def last_objects(edge_id: str, camera_id: str, limit: int = 10):
    """
    Return the UNIQUE label names seen in the last <limit> events
    for this camera, newest first.
    """
    data = await store.snapshot()
    events = [d for d in data.get(edge_id, []) if d["camera_id"] == camera_id][:limit]

    if not events:
        raise HTTPException(status_code=404,
                            detail=f"No events for edge={edge_id} camera={camera_id}")

    # flatten -> set -> list preserves insertion order in Py3.7+
    seen = []
    for e in events:
        for lbl in e.get("labels", []):
            if lbl not in seen:
                seen.append(lbl)

    return seen

@app.get("/frames/{edge_id}/{camera_id}", response_model=List[Dict])
async def last_frames(edge_id: str, camera_id: str, limit: int = 10):
    """
    Return up to <limit> frames (newest first). Each item:
      { "labels": [...], "image": "<base-64 jpg or null>" }
    """
    data = await store.snapshot()
    events = [d for d in data.get(edge_id, []) if d["camera_id"] == camera_id][:limit]

    if not events:
        raise HTTPException(status_code=404,
                            detail=f"No events for edge={edge_id} camera={camera_id}")

    return [
        {
            "labels": e.get("labels", []),
            "image":  e.get("annotated_jpg_base64"),
        }
        for e in events
        if e.get("annotated_jpg_base64")        # keep only frames that have images
    ]
