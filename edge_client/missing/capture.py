import cv2

_BACKENDS = [cv2.CAP_FFMPEG, cv2.CAP_GSTREAMER, 0]


def open_capture(source: str | int) -> cv2.VideoCapture:
    """
    Try various OpenCV back-ends until one opens the stream successfully.
    Raises RuntimeError if **all** fail.
    """
    for be in _BACKENDS:
        cap = cv2.VideoCapture(int(source) if str(source).isdigit() else source, be)
        if cap.isOpened():
            return cap
    raise RuntimeError(
        f"Cannot open video source: {source!r}. "
        "Check that FFmpeg/GStreamer is installed and the URL is reachable."
    )
