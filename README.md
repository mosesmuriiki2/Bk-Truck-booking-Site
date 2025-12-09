# BK Roadshow Trucks

A clean, modern Django site to manage and book roadshow trucks, including extras like sound systems, screens, and dance teams. Admins can manage trucks, drivers, maintenance (fields can be extended), and approve or reject bookings.

## Features
- Browse available trucks with pricing and features
- Create bookings with date range, routes, purpose, and extras
- Booking status workflow: reserved → approved/rejected
- User auth: login, register, view "My Bookings"
- Django admin for trucks, drivers, extras, and bookings

## Tech Stack
- Django 6
- Tailwind CDN for modern UI
- Whitenoise for static files in production

## Local Setup
1. Ensure Python 3.11+ (your environment is Python 3.14)
2. Create a virtual environment and install deps:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. Run migrations and start the server:
   ```powershell
   .\.venv\Scripts\python.exe manage.py makemigrations
   .\.venv\Scripts\python.exe manage.py migrate
   .\.venv\Scripts\python.exe manage.py runserver
   ```
4. Visit `http://127.0.0.1:8000/`
5. Create a superuser to access admin:
   ```powershell
   .\.venv\Scripts\python.exe manage.py createsuperuser
   ```

## Seeding Data (optional)
Use Django admin to add Drivers, Trucks, and Extras. Then try booking from the truck detail page.

## Deployment (Vercel)
Vercel supports Python via serverless functions. A minimal approach is to expose Django’s WSGI app through an `api` endpoint. This project includes a sample config. Note: for production, consider a platform built for long-running apps (Render, Railway) or Vercel with serverless constraints.

### Steps
1. Install Vercel CLI and log in:
   ```bash
   npm i -g vercel
   vercel login
   ```
2. Create a `VERCEL` environment with Python build using `@vercel/python`.
3. Ensure `requirements.txt` is present; Vercel will install from it.
4. Static files are served by Whitenoise.

### Caveat
Django on Vercel runs as serverless requests via WSGI/ASGI and is stateless. Use a managed database (e.g., Neon/Postgres or PlanetScale/MySQL) and configure `DATABASES` accordingly. SQLite is fine for local dev only.

## Structure
```
accounts/    # login, register
bookings/    # booking model, admin, my bookings view
trucks/      # trucks, drivers, extras, list/detail views
bkbookingtrucks/  # project settings and urls
templates/   # base and app templates
static/      # optional; add your assets
```

## Next Improvements
- Add maintenance, insurance, and driver scheduling models
- Availability calendar view
- Admin dashboards and CSV exports
- Email notifications for booking approvals
- Switch to Postgres and add environment-based settings