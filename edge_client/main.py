import logging, time, sys
import cv2

from src import config
from missing import capture
from logic import inference, sender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("edge_client")

def run() -> None:
    log.info("Starting edge-client with settings: %s", config.as_dict())

    cap = capture.open_capture(config.URL_CAMERA)
    log.info("Camera opened – processing stream...  Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
            ok, frame = cap.read()
            if not ok:
                log.warning("Frame grab failed – sleeping .5 s")
                continue

            payload, _ = inference.run_inference(frame)

            # send only if we actually detected something
            if payload.get("labels"):
                log.info("Detected: %s", payload["labels"])
                try:
                    sender.post_detection(payload)
                except Exception as exc:  # noqa: BLE001
                    log.error("POST failed: %s", exc)
            else:
                log.info("No detections this frame")

    except KeyboardInterrupt:
        log.info("Interrupted by user – shutting down.")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
