# Gardening-Project-Final

A full‑stack web application that helps gardening enthusiasts track plant health, receive care reminders, join gardening groups, and share resources. Built with **Django** (Python) for the backend and **HTML/CSS** for the frontend.

---

## Overview

The Gardening Project provides a centralized hub where users can:

- Record health data for their plants.
- Set automated watering/fertilizing reminders.
- Join or create gardening groups and discussion threads.
- Receive personalized plant care recommendations.
- Upload and view images (e.g., profile pictures, plant photos).

All data is stored in a relational database and served through a clean, responsive HTML interface.

---

## Features

| ✅ | Feature |
|---|---------|
| ✔️ | **Plant Health Tracking** – Log measurements, notes, and photos for each plant. |
| ✔️ | **Automated Reminders** – Email/notification reminders for watering, fertilizing, and pruning. |
| ✔️ | **User Profiles** – Upload profile pictures (`media/profile_pics/DB.png`, `day.png`). |
| ✔️ | **Gardening Groups** – Create/join groups, discuss topics, and share resources. |
| ✔️ | **Recommendations Engine** – Suggest care actions based on plant species and health data. |
| ✔️ | **Notifications** – Real‑time alerts for upcoming tasks and group activity. |
| ✔️ | **Discussion Boards** – Threaded conversations within groups. |
| ✔️ | **Resource Library** – Upload PDFs, images, and links for community reference. |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, Django 4.x |
| **Database** | SQLite (default) – easily switchable to PostgreSQL/MySQL |
| **Frontend** | HTML5, CSS3 (static templates) |
| **Media Storage** | Local `media/` directory (profile pictures, plant images) |
| **Version Control** | Git (GitHub) |
| **Deployment** | Any WSGI‑compatible server (e.g., Gunicorn + Nginx) |

---

## Installation

> **Prerequisite:** Python 3.9+ and Git must be installed on your machine.

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/Gardening-Project-Final.git
cd Gardening-Project-Final

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install --upgrade pip
pip install django  # Add any additional packages to a requirements.txt later

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create a superuser (optional, for admin access)
python manage.py createsuperuser

# 6️⃣ Collect static files (if you plan to serve them via a web server)
python manage.py collectstatic
```

> **Note:** The repository does not include a `requirements.txt`. Feel free to generate one with `pip freeze > requirements.txt` after installing all needed packages.

---

## Usage

```bash
# Run the development server
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0