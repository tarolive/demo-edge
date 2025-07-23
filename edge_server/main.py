import subprocess, sys, threading, time, logging
from pathlib import Path
import uvicorn
from src import config, api

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger("edge_server")

def run_uvicorn():
    uvicorn.run(
        api.app,
        host=config.HOST,
        port=config.API_PORT,
        log_level="info",
        access_log=False,
    )

def run_streamlit() -> None:
    """Spawn Streamlit in a subprocess."""
    ui_file = (Path(__file__).parent / "src" / "ui.py").as_posix()  # …/src/ui.py

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.headless=true",
        "--server.port", str(config.STREAMLIT_PORT),
        "--logger.level", "error",     # quiet logs; drop if you want INFO
        ui_file                         # target .py – must come *after* the flags
    ]
    subprocess.run(cmd, check=True)

def main() -> None:
    log.info("Launching edge_server with settings: %s", config.as_dict())

    # FastAPI in background thread
    api_thread = threading.Thread(target=run_uvicorn, daemon=True)
    api_thread.start()

    # Let Uvicorn print its banner first
    time.sleep(1.0)

    # Streamlit blocks until Ctrl-C
    run_streamlit()


if __name__ == "__main__":
    main()
