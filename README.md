# PUP MOA & Internship Tracker

A comprehensive Django-based web application designed to streamline the process of managing Memorandum of Agreements (MOAs) and internship placements for the Polytechnic University of the Philippines (PUP). Developed specifically to support the College of Engineering.

## Features

- **Student Profiles & Authentication**: Secure registration and login system capturing Student Numbers, Year Levels, and specific Engineering Courses via a scalable `StudentProfile` model.
- **Searchable Dashboard**: Centralized tagging and search functionality for students to filter through active PUP partner companies.
- **Application & MOA Tracking**: End-to-end tracking of Internship Applications and manual MOA Requests.
- **Custom Admin Portal**: A protected, custom-built management dashboard designed exclusively for university administrators (restricted to `is_staff`) to overview and approve/reject MOA workflows efficiently.
- **Automated Email Notifications**: Native Django email triggers that notify students the exact moment their application or MOA request status is changed by the administration.
- **Responsive Design**: Built natively with Tailwind CSS via CDN and the Tailwind Forms plugin for extremely fast, modern, mobile-friendly UI rendering.

## Getting Started

Follow these steps to set up your local development environment.

### 1. Prerequisites
- **Python 3.14+**
- **[Pipenv](https://pipenv.pypa.io/en/latest/)** (Recommended for dependency isolation)

### 2. Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MOA-tracker-project
   ```

2. **Install Dependencies:**
   This project uses `pipenv` to manage the virtual environment and requirements.
   ```bash
   pipenv install
   ```

3. **Initialize the Environment:**
   Enter the virtual environment and navigate to the project core:
   ```bash
   pipenv shell
   cd core
   ```

4. **Database & Admin Setup:**
   Apply migrations and create a superuser for administrative access:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

---

## Development Workflow

To develop effectively, you will need to run multiple services simultaneously. It is recommended to use a split-terminal or multiple terminal tabs.

### 1. Running the Services

| Service | Command (from `core/` directory) | Purpose |
| :--- | :--- | :--- |
| **Web Server** | `python manage.py runserver` | Main application logic (Dashboard, API, etc.) |
| **Task Cluster** | `python manage.py qcluster` | **Required** for notifications, alerts, and async emails. |

> [!NOTE]
> Since we use the ORM broker, `qcluster` is essential for processing the background task queue. If not running, emails and notifications will appear to "hang" or fail.

### 2. Running Tests

Automated testing is critical before pushing changes. All tests should be run from the `core/` directory.

- **Run all tests:**
  ```bash
  python manage.py test
  ```
- **Run tests for a specific app:**
  ```bash
  python manage.py test accounts
  ```
- **Run manual validation scripts:**
  There are additional scripts in `scratch/` for specific logic verification (e.g., expiry logic):
  ```bash
  python scratch/test_expiry.py
  ```

### 3. Accessing the Dashboards

- **Student/Main View:** [http://localhost:8000](http://localhost:8000)
- **University Admin Portal:** [http://localhost:8000/dashboard/admin/](http://localhost:8000/dashboard/admin/)
- **Django Default Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Usage Guide

- **Emails & Notifications**: In development mode, emails are printed directly to the terminal running the `runserver` command (using the Console Backend).
- **Admin Portal**: Restricted to users with `is_staff=True`. Use the Custom Admin Dashboard to manage MOA approvals and verify notifications.

## License

This project is licensed under the terms of the MIT license.