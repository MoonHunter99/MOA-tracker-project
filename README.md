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

### Prerequisites

- Python 3.8+
- Django 6.0+
- **[Pipenv](https://pipenv.pypa.io/en/latest/)** (for dependency management)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MOA-tracker-project
   ```

2. **Initialize pipenv and install dependencies:**
   Instead of using traditional `venv` and `requirements.txt`, this project relies on `pipenv`.
   ```bash
   pipenv install
   ```

3. **Enter the virtual environment:**
   ```bash
   pipenv shell
   cd core
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (Required for Admin Portal access):**
   ```bash
   python manage.py createsuperuser
   ```
   *Make sure your superuser has `is_staff=True` to access the custom university admin dashboard.*

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. Access the main application at `http://localhost:8000`.
8. Access the University Admin Portal at `http://localhost:8000/dashboard/admin/`.

## Usage

- **Student Login**: Register a new student account to submit requests and applications. Use the search bar to locate specific companies.
- **Admin Portal**: Log in using the superuser account and click the yellow **Admin Portal** button to manage pending requests and auto-dispatch status emails. Emails will instantly print directly to the running console window instead of SMTP while in development mode.

## License

This project is licensed under the terms of the MIT license.