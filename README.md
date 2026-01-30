# Employee Task Management Platform

A robust Django-based platform for managing projects, assigning tasks, and tracking employee performance with real-time notifications and AI-assisted insights.

## Features
- **Role-based Access Control**: Admins, Managers, and Employees.
- **Project & Task Management**: Full CRUD operations for project lifecycle.
- **Real-Time Notifications**: Instant alerts using WebSockets (Django Channels).
- **Analytics Dashboard**: Data visualization with Chart.js and data processing with pandas.
- **AI Insights**: Automated task prioritization and sentiment analysis for comments.
- **Reporting**: Export reports to CSV, Excel, and PDF.
- **Audit Logs**: Comprehensive activity tracking for security.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install django pandas openpyxl xhtml2pdf channels daphne
   ```

2. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**:
   ```bash
   python manage.py runserver
   ```
   *Note: For WebSockets, ensure you use `daphne` or a compatible ASGI server in production.*

5. **Running Tests**:
   ```bash
   python manage.py test
   ```

## Development Plan
This project was built over a 10-day sprint, covering everything from core architecture to advanced AI features and real-time communication.
