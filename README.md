# Shortify - Django Link Shortener

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)

Shortify is a **Django-based link shortener** that allows users to generate short URLs, track analytics, generate QR codes, and manage their links efficiently.

---

## Features

- Generate **short URLs** for long links.
- Support **custom aliases** for short links.
- **Anonymous and registered user support**.
- **Track clicks** and **unique visitors**.
- **QR code generation** for all short URLs.
- Set **expiration dates** and **password protection** for links.
- Responsive **dashboard** to manage links and view analytics.
- Copy short URL to clipboard.
- Export analytics data.

---


## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/shortify.git
cd shortify
```

2. **Create a virtual environment:**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4. **Apply migrations:**
```bash
python manage.py migrate
```
5. **Create a superuser:**
```bash
python manage.py createsuperuser
```
6. **Run the development server:**
```bash
python manage.py runserver
```

7. **Open your browser at http://127.0.0.1:8000/**


---

## Usage

- Create an account or use anonymously.
- Shorten URLs using the landing page.
- Manage your links via the dashboard.
- View analytics for each link including click count, unique visitors, and QR codes.
- Download QR codes for sharing.

---

## Tech Stack

- **Backend:** Django 5.2.7
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** SQLite (default) / Postgres compatible
- **Others:** qrcode for QR code generation

---

## Contributing
Contributions are welcome!
- Fork the repository
- Create a new branch (git checkout -b feature/YourFeature)
- Commit your changes (git commit -m 'Add some feature')
- Push to the branch (git push origin feature/YourFeature)
- Open a Pull Request

---