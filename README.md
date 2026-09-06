# Musify_H25

Vue frontend + Flask API + MySQL. Portfolio demo stack: GitHub Pages, Render, external MySQL.

## Local run

Backend:

```
pip install -r backend/requirements.txt
python backend/main.py
```

Frontend:

```
cd frontend
npm install
npm run dev
```

Local env vars:

```
DB_PASSWORD
DB_NAME
KEY_PASSWORD
EMAIL_PASSWORD
```

## Demo login

`admin` / `demo123`

Signup stays disabled unless `EMAIL_PASSWORD` is set. Render free web services block SMTP.

## Deploy

1. Create a free MySQL database.
2. Import `database/schema.sql`, then `database/seed_demo.sql`.
3. Set `KEY_PASSWORD=demo-key-password` so the seeded admin password decrypts.
4. Create a Render web service from this repo:
   - Build: `pip install -r backend/requirements.txt`
   - Start: `gunicorn backend.main:app --bind 0.0.0.0:$PORT`
   - `PYTHONPATH=.`
   - `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `FRONTEND_ORIGIN`
5. Enable GitHub Pages via Actions.
6. Set repository variables:
   - `VITE_API_URL` = Render API URL
   - `VITE_BASE` = `/Musify_H25/` for a project Pages site, or `/` for a user site
7. Optional ML: add `backend/requirements-ml.txt` to the Render build. First recommendation request is slow.

The free Render API sleeps after 15 minutes idle. The first request after sleep can take about a minute.

Health check: `GET /health`
