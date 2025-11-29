## PRBS System - Backend and Frontend

### Prerequisites
- Python 3.11+ (Linux)
- Node.js 18+

### Backend (Django)
1. Create and activate a venv (Linux):
```bash
python3 -m venv .venv && source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run server:
```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Frontend (Next.js)
1. Install and run:
```bash
cd next-frontend
npm install
npm run dev
```
2. Visit http://localhost:5174. Configure backend base URL with `NEXT_PUBLIC_API_BASE` env var.

### Postman
- Import `PRBS_API_Collection.json` for full API coverage.
- Import `PRBS_Frontend_Collection.json` for quick smoke endpoints including the industry ranking.

### Notes
- Ensure CORS is enabled (development is already set in `config/settings.py`).
- Login flows expect JWT; set `auth_token` env in Postman or log in via API to obtain one.

