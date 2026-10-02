# EduGenie — deployment-ready web assistant

A Flask web app with an HTML/CSS/JavaScript interface. Features include text commands, browser speech input, spoken responses, date/time, Wikipedia summaries, jokes, and opening Google/YouTube.

## Run locally (Windows)
1. Install Python 3.10 or newer.
2. Extract this ZIP and open a terminal in the `EduGenie_Ready` folder.
3. Create and activate a virtual environment:
   - `py -m venv .venv`
   - `.venv\\Scripts\\activate`
4. Install packages: `pip install -r requirements.txt`
5. Start: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

## Deploy online
This project is prepared for a Python-compatible host that supports a GitHub repository and a web service.

1. Create a GitHub repository.
2. Upload the *contents* of this folder (app.py, Edugenie.py, requirements.txt, Procfile, runtime.txt, templates, static, README).
3. In your hosting provider, create a new **Web Service** and connect that repository.
4. Set the build/install command to `pip install -r requirements.txt`.
5. Set the start command to `gunicorn app:app`.
6. Deploy. Open the public URL supplied by the host (usually an `https://...` address).

Do not use Flask's development server for public hosting. The included Procfile is for platforms that read it; the explicit Gunicorn start command works on many Python hosts.

## API
- `GET /api/health` — backend health check
- `POST /api/command` — JSON body, e.g. `{"command":"time"}`

## Notes
- No database or AI API key is required for the included features.
- Wikipedia needs an internet connection.
- Voice input depends on browser support and microphone permission; speech recognition generally works best in Chrome/Edge over HTTPS or localhost.
- Many free hosts use temporary filesystems or sleep when idle. The assistant-name change may not persist after a restart unless the host provides persistent storage.
