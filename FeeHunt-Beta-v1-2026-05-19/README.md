# FeeHunt

FeeHunt is a beta desktop-friendly Streamlit app for scanning Gmail messages,
finding subscriptions, promotional email, newsletters, shop messages, and
possible financial-risk messages.

## Run From Source

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Copy `credentials.example.json` to `credentials.json` and fill it with your
   local Gmail OAuth client details.
3. Run the app:

```powershell
streamlit run app.py
```

The app opens on `http://localhost:8501`.

## Run The EXE

Open:

```text
dist_beta/FeeHunt/FeeHunt.exe
```

The packaged app starts a local Streamlit server on `http://localhost:8501`.
If `credentials.json` is missing, FeeHunt shows the folder where the local OAuth
file must be placed.

## Sensitive Local Files

These files are local user or developer data and must not be committed to Git,
published, or shared publicly:

- `credentials.json` - developer OAuth client file for Gmail access.
- `token.json` - local user authorization token created after Gmail login.
- `last_scan_results.json` - local user email scan results.
- `feehunt_settings.json` - local user settings and cleanup preferences.
- `.streamlit/secrets.toml` - local Streamlit secrets, if used.

The project `.gitignore` excludes these files. Before distributing a build,
review `FeeHunt.spec` and the generated `dist*` folders to confirm that no
private user files are included.

## Beta Note

FeeHunt is currently beta software. Gmail cleanup actions can affect real email,
so test carefully and keep sensitive files local.
