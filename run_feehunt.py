import os
import sys
import time
import webbrowser
from pathlib import Path
from threading import Timer
from urllib.request import urlopen


def configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def safe_print(value="", *, flush: bool = False) -> None:
    try:
        encoding = sys.stdout.encoding or "utf-8"
        text = str(value).encode("utf-8", errors="replace").decode("utf-8", errors="replace")
        text = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
        sys.stdout.write(text + "\n")
        if flush:
            sys.stdout.flush()
    except Exception:
        pass


configure_console_encoding()


def get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        internal_dir = exe_dir / "_internal"

        if internal_dir.exists():
            return internal_dir

        return exe_dir

    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()
APP_FILE = APP_DIR / "app.py"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = "8501"
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

# Labai svarbu PyInstaller aplinkoje:
# pridedame _internal aplanką į import kelią
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from translations import t

# Streamlit konfigūracija
os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

from streamlit.web import cli as stcli


def open_browser():
    webbrowser.open(SERVER_URL)


def open_browser_when_ready() -> None:
    for _ in range(60):
        try:
            with urlopen(SERVER_URL, timeout=1):
                webbrowser.open(SERVER_URL)
                return
        except Exception:
            time.sleep(0.5)


def server_is_running() -> bool:
    try:
        with urlopen(SERVER_URL, timeout=1):
            return True
    except Exception:
        return False


def main():
    os.chdir(APP_DIR)

    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        from main import main as scan_main

        scan_main()
        return

    if not APP_FILE.exists():
        safe_print(t("runner.app_missing").format(path=APP_FILE))
        safe_print(t("runner.check_internal"))
        input(t("runner.press_enter"))
        sys.exit(1)

    if server_is_running():
        safe_print(f"FeeHunt is already running at {SERVER_URL}", flush=True)
        webbrowser.open(SERVER_URL)
        return

    # Show a branded "loading" page immediately so the user gets feedback while
    # the Streamlit server boots (otherwise the window stays blank for several
    # seconds and looks frozen). The page polls the server and redirects itself
    # once it answers. If the page is missing (e.g. dev run), fall back to
    # opening the app URL once the server is reachable.
    loading_page = APP_DIR / "loading.html"
    if loading_page.exists():
        webbrowser.open(loading_page.as_uri())
    else:
        Timer(0.5, open_browser_when_ready).start()

    sys.argv = [
        "streamlit",
        "run",
        str(APP_FILE),
        "--global.developmentMode=false",
        f"--server.port={SERVER_PORT}",
        f"--server.address={SERVER_HOST}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
