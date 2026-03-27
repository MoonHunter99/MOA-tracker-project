# PUP MOA & Internship Tracker

A comprehensive Django-based web application designed to streamline the process of managing Memorandum of Agreements (MOAs) and internship placements for the Polytechnic University of the Philippines (PUP).

## Features

- **User Authentication**: Secure login and registration system for students and companies.
- **Dashboard**: Centralized dashboard for managing internship applications and MOA processes.
- **Application Tracking**: Track the status of internship applications from submission to approval.
- **MOA Management**: Manage the creation and tracking of MOA documents between the university and partner companies.
- **Responsive Design**: Built with Tailwind CSS for a modern, mobile-friendly interface.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 6.0+

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd core
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://localhost:8000`.

## Usage

- **Login**: Use the credentials created during the superuser setup or register a new account.
- **Dashboard**: Navigate to the dashboard to view and manage applications and MOAs.

## License

This project is licensed under the terms of the MIT license.