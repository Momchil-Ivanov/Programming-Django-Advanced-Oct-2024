# Excel Tips and Tricks App

## Overview
This Django-based application serves as a platform where users can view, create, and manage Excel tips and tricks.
It features robust functionalities for categorizing, tagging, and managing user profiles,
with comprehensive role-based authentication and authorization. The app is deployed on Microsoft Azure
and utilizes PostgreSQL for data storage.

## Installation

### 1. Clone the Repository
Begin by cloning the repository to your local development environment:
   ```bash
git clone -b excel_tips_and_tricks https://github.com/Momchil-Ivanov/Programming-Django-Advanced-Oct-2024.git
   ```
Then navigate to the project directory:
   ```
cd Programming-Django-Advanced-Oct-2024
   ```


### 2. Install Dependencies
Install the necessary Python dependencies as specified in the requirements.txt file:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure Environment Variables
Create a .env file in the root directory of the project and populate it with the following environment variables.
These are crucial for application configuration, including database connection settings and email service configuration.

# .env file content
SECRET_KEY='your-django-secret-key'
DB_NAME=excel_tips_and_tricks
DB_USER=your-db-username
DB_PASS=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1
EMAIL_HOST=in-v3.mailjet.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='your-mailjet-user'
EMAIL_HOST_PASSWORD='your-mailjet-password'
COMPANY_EMAIL='your-email@gmail.com'
API_KEY='your-openweathermap.org-api-key'

### 4. Set Up PostgreSQL Database
Create a PostgreSQL database named "excel_tips_and_tricks" on your local machine or in the cloud.

### 5. Apply Migrations
Run Django migrations to set up the necessary database tables:
   ```
python manage.py migrate
   ```

### 6. Create a Superuser
Create a superuser to access the Django admin panel:
   ```
python manage.py createsuperuser
   ```

### 7. Run the Development Server
To start the Django development server locally:
   ```
python manage.py runserver
   ```

Access the app in your browser at http://127.0.0.1:8000/.

### Azure Deployment

The project is deployed on Microsoft Azure and can be accessed at
https://exceltipsandtricks-duc5cncrakhjfthr.italynorth-01.azurewebsites.net/.
