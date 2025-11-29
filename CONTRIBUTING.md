# Prudential Project Setup & Collaboration Guide

# Project Setup & Pushing Changes

## Setting Up Locally

### Backend(`prudential-backend`)

```bash
# Clone the repo
git clone https://github.com/NUST-SECZim/prudential.git

# Navigate to the backend folder
cd prudential/prudential-backend

# Set up virtual environment
python -m venv prudential_env
prudential_env\Scripts\activate  # Use `source prudential_env/bin/activate` on Linux or Mac

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

### Frontend(`prudential-frontend`)

```bash
# Navigate to the frontend folder
cd prudential/prudential-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Current Folder Structure

### Backend

```bash
prudential-back/
├── apps/
│ ├── __init__.py
│ ├── auth_module/
│ └── compliance_module/
├── config/
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── prudential_env/
├── .gitignore
├── CONTRIBUTING.md
├── manage.py
└── requirements.txt
```

### Frontend

```bash
prudential-frontend/
├── public/
├── src/
│   ├── app/                # App router structure
│   │   └── page.tsx        # Landing page (can be split into layouts, etc.)
│   ├── components/         # Reusable UI components
│   ├── features/           # Domain-specific features
│   │   ├── auth/           # e.g., login, register, auth utils
│   │   └── compliance/     # compliance-related UIs
│   ├── hooks/              # Custom hooks
│   ├── lib/                # API calls, util functions
│   ├── styles/             # Global and module styles
│   └── types/              # TypeScript types
├── .gitignore
├── CONTRIBUTING.md
├── .eslintrc.json
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

# Coding Style Guide – Prudential & AML Teams

## General Principles

- Consistency is more important than cleverness.
- Keep functions small and focused (Single Responsibility).
- Use descriptive, meaningful names for variables and functions.
- Write comments **only** when necessary — clean code is self-explanatory.

---

## Django (Python)

### Structure

- Use `apps/` folder to contain domain-specific apps.
- Use `config/settings/` for settings split (base/dev/prod).

### Conventions

- Snake_case for variables and functions.
- PascalCase for classes.
- Constants in ALL_CAPS.
- Use `.env` for secrets and DB config

---

## Next.js (TypeScript)

### Structure

- Use `src/` to contain everything: `pages/`, `components/`, `lib/`, `types/`, etc.
- Keep components small and reusable.
- Group related files into feature folders if needed.

### Conventions

- CamelCase for components and functions.
- PascalCase for React components.
- Use `interface` for defining prop types.
- Prettier + ESLint should auto-format your code.

---

## Tools & Linting

- Set up Prettier and ESLint in both projects.

---

_“Clarity is kindness.” – Kent Beck_

## Pushing Changes to Remote

```bash
# Check which files changed
git status

# Stage your changes
git add .

# Commit with a meaningful message
git commit -m "[auth] implement login UI and API integration"

# Push to development or your feature branch
git push origin development
```

## Adding New Features

- Each domain or module (auth, compliance, etc.) goes into features/<module>.
- Reusable buttons/forms go into components/.
- Use hooks/ for logic like useAuth, useFetch.
- Keep styling modular (Tailwind + scoped CSS modules if needed).

## Branching Strategy

### Core Branches

- `production` → Stable, release-ready code.
- `development` → Integrates all feature branches; staging ground.

### Additional Branches

- `feature/<name>` → For specific features (e.g., feature/login-page).
- `bugfix/<name>` → For fixing specific issues.
- `hotfix/<name>` → Urgent patches directly off production.

## Workflow

1. Pull latest development:

   - git checkout development
   - git pull origin development

2. Create feature branch:

   - git checkout -b feature/auth-login

3. Push work:

   - git push origin feature/auth-login

4. Create a Pull Request (PR) to development.

5. Team reviews → If approved, merge.

6. PR from development to production happens only for a release.

## Tracking Team Work

Use WhatsApp for communication. The following needs to be communicated;

1. Pushes to remote
2. Pull requests
3. Use of additional tools
4. Anything that needs clarification

# Love and Light coders!
