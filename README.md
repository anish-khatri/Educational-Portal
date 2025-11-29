# Anish-fyp

This is a Django project for managing college admissions.

## Setup Instructions

1. Run migrations:

   python manage.py migrate --run-syncdb

2. Seed initial user data:

   python manage.py seed_users

3. Change directory to the sms app:

   cd sms

4. Run the development server:

   python manage.py runserver
