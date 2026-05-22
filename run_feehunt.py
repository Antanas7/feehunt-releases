import os
import sys
import webbrowser
from pathlib import Path
from threading import Timer


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
    webbrowser.open("http://localhost:8501")


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

    Timer(2.0, open_browser).start()

    sys.argv = [
        "streamlit",
        "run",
        str(APP_FILE),
        "--global.developmentMode=false",
        "--server.port=8501",
        "--server.address=localhost",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
