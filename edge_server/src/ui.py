import os, requests, streamlit as st, base64, io
from PIL import Image
from datetime import datetime
from typing import Dict, List
from streamlit_autorefresh import st_autorefresh

EDGE_ID   = os.getenv("EDGE_ID", "test-edge")
CAMERA_ID = os.getenv("CAMERA_ID", "test-cam")
API_ROOT  = os.getenv("API_ROOT", "http://localhost:8000")
REFRESH_SEC = 2

st.set_page_config(page_title="Edge-Server Dashboard", layout="wide")

def pretty(ts_iso: str | None) -> str:
    if not ts_iso:
        return ""
    dt = datetime.fromisoformat(ts_iso.replace("Z", "+00:00")).astimezone()
    short = dt.strftime("%d %b %Y %H:%M")
    full  = dt.strftime("%d %b %Y %H:%M:%S %Z")
    return f"<span title='{full}'>{short}</span>"

def fetch_events(limit: int = 10) -> List[dict]:
    url = f"{API_ROOT}/frames/{EDGE_ID}/{CAMERA_ID}?limit={limit}"
    r = requests.get(url, timeout=3)
    if r.status_code == 404:
        return []                      # no events yet
    r.raise_for_status()
    return r.json()                    # list[{"labels": [...], "image": "..."}]

events = fetch_events(1)

if not events:
    st.info("No detections received yet …")
else:
    with st.expander(f"{CAMERA_ID} — {len(events)} recent frames", expanded=True):
        for ev in events:
            label_txt = ", ".join(ev["labels"]) if ev["labels"] else "—"
            st.markdown(f"{pretty(None)} **{label_txt}**", unsafe_allow_html=True)

            if ev["image"]:
                img = Image.open(io.BytesIO(base64.b64decode(ev["image"])))
                st.image(img, use_column_width=True)

# auto-refresh
st_autorefresh(interval=REFRESH_SEC * 1000, key="auto")
