# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules


block_cipher = None
project_dir = Path.cwd()

streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all("streamlit")


required_datas = [
    ("app.py", "."),
    ("main.py", "."),
    ("config.py", "."),
    ("feehunt_analyzer.py", "."),
    ("phishing_detector.py", "."),
    ("gmail_auth.py", "."),
    ("gmail_actions.py", "."),
    ("licensing.py", "."),
    ("local_memory.py", "."),
    ("subscription_actions.py", "."),
    ("time_utils.py", "."),
    ("translations.py", "."),
    ("translations_extra.py", "."),
    ("translations_full.py", "."),
    ("translations_v112.py", "."),
    ("user_state.py", "."),
    ("requirements.txt", "."),
    ("credentials.json", "."),
    ("loading.html", "."),
    ("scan-earth.jpg", "."),
    (".streamlit/config.toml", ".streamlit"),
]

for forbidden_file in (
    "token.json",
    "last_scan_results.json",
    "feehunt_settings.json",
    "feehunt_rules.json",
    "feehunt_memory.json",
    "feehunt_license.json",
    "feehunt_session.json",
):
    if any(Path(source).name == forbidden_file for source, _target in required_datas):
        raise RuntimeError(f"Do not package user data file: {forbidden_file}")

    root_candidate = project_dir / forbidden_file
    if root_candidate.exists():
        raise RuntimeError(
            f"Privacy preflight failed: remove local user data from the project root before building: {root_candidate}"
        )


# Šie paketai turi būti nukopijuoti į _internal
a = Analysis(
    ["run_feehunt.py"],
    pathex=[str(project_dir)],
    binaries=streamlit_binaries,
    datas=required_datas + streamlit_datas,
    hiddenimports=[
        "google",
        "google.auth",
        "google.auth.transport",
        "google.auth.transport.requests",
        "google.auth.transport.httplib2",
        "google.oauth2",
        "google.oauth2.credentials",
        "googleapiclient",
        "googleapiclient.discovery",
        "googleapiclient.errors",
        "google_auth_oauthlib",
        "google_auth_oauthlib.flow",
        "httplib2",
        "dateutil",
        "dateutil.parser",
    ]
    + streamlit_hiddenimports
    + collect_submodules("google")
    + collect_submodules("google.auth")
    + collect_submodules("google.oauth2")
    + collect_submodules("googleapiclient")
    + collect_submodules("google_auth_oauthlib"),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FeeHunt",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon="icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="FeeHunt",
)
