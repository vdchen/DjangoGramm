# DjangoGramm



## Features

- **Multi-Image Uploads**: Post multiple photos at once using a Bootstrap carousel.
- **Dynamic Tagging System**: Type tags as a single string; the system automatically parses, cleans, and generates unique slugs.
- **Asynchronous Likes**: Real-time "Like" functionality using AJAX (Fetch API) to avoid page reloads.
- **User Profiles**: Automatic profile creation via Django Signals.
- **Search & Filtering**: Filter the feed by specific hashtags.

## Tech Stack
- **Backend**: Django 5.x, PostgreSQL
- **Frontend**: Bootstrap 5, JavaScript (Fetch API)
- **Utilities**: Pillow, Django-Imagekit, Django-Cleanup

## Installation & Setup

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
```
3.Install dependencies:
```bash
pip install -r requirements.txt
```
4.Run migrations:
```bash
python manage.py migrate
```
5.Start the server:
```bash
python manage.py runserver
```