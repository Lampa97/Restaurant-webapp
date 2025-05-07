# Restaurant Reservation System

This project is a **Restaurant Reservation System** built with **Django**. It allows users to make reservations, manage restaurant services, and handle user accounts. The system also integrates with Celery for task scheduling and Redis for caching and message brokering.

*** The website is available at address https://iron-hoof.com ***

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Applications](#applications)
4. [Dependencies](#dependencies)
5. [Environment Variables](#environment-variables)
6. [Setup Instructions](#setup-instructions)
   - [Docker Setup](#docker-setup)
   - [Running the Server](#running-the-server)
7. [Features](#features)
8. [Static and Media Files](#static-and-media-files)
9. [Logging](#logging)
10. [License](#license)

---

## Project Overview

The **Restaurant Reservation System** is designed to:
- Allow users to book tables at a restaurant.
- Manage restaurant services and reservations.
- Send email notifications for reservations.
- Schedule periodic tasks using Celery.
- Cache data for improved performance using Redis.

---

## Project Structure

The project follows the standard Django structure:

```
├── config/                # Main project configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI application
├── restaurant/            # Core app for restaurant management
├── reservation/           # App for handling reservations
├── services/              # App for additional restaurant services
├── users/                 # Custom user model and authentication
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── media/                 # Media files (uploads)
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Dependency management (optional)
├── uv.lock                # Dependency lock file (optional)
├── .env                   # Environment variables
```

---

## Applications

### Core Apps

1. **restaurant**: 
   - Manages restaurant details and operations.
   - Displays restaurant information to users.

2. **reservation**: 
   - Handles table reservations and booking logic.
   - Allows users to book tables and view their reservations.

3. **services**: 
   - Manages additional services offered by the restaurant.
   - Displays available services to users.

4. **users**: 
   - Implements a custom user model and authentication.
   - Allows users to register, log in, and manage their accounts.

### User Features:
- **Home Page**: View restaurant details and available services.
- **Reservation System**: Book tables, view, and manage reservations.
- **User Account**: Register, log in, and manage personal details.
- **Admin Panel**: For administrators to manage users, reservations, and services.

### Third-Party Apps
1. **django_celery_beat**: Periodic task scheduling.
2. **django_celery_results**: Stores Celery task results.

---

## Dependencies

The project uses the following key dependencies:
- **Django**: Web framework.
- **Celery**: Task queue for asynchronous tasks.
- **Redis**: Message broker and caching backend.
- **psycopg2**: PostgreSQL database adapter.
- **colorlog**: Colored logging for better debugging.

For a full list of dependencies, see `requirements.txt`.

---

## Environment Variables

The project uses a `.env` file to manage sensitive information. Below is an example of the required variables:

```dotenv
SECRET_KEY=your-secret-key
DEBUG=True

POSTGRES_DB=Restaurant
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

SERVER_IP=your-server-ip (optional)

DOMAIN_NAME=your-domain-name (optional)

CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

---

## Setup Instructions

### Docker Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Lampa97/Restaurant-webapp.git
   cd Restaurant-webapp
   ```

2. **Create a `.env` File**:
   Copy the example above and save it as `.env` in the project root.

3. **Build and Start Docker Containers**:
   ```bash
   docker-compose up -d --build
   ```

4. **Apply Migrations**:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   docker-compose exec backend python manage.py createadmin
   ```

6. **Create a Manager group**:
   ```bash
   docker-compose exec backend python manage.py create_managers_group
   ```

7. **Create a restaurant tables set**:
   ```bash
   docker-compose exec backend python manage.py create_tables
   ```
```

---

### Running the Server

Once the containers are up, the application will be available at:
- **Backend**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin`

---

## Features

1. **User Authentication**:
   - Custom user model.
   - Login, logout, and registration.

2. **Reservation Management**:
   - Book tables with time slots.
   - View and manage reservations.

3. **Task Scheduling**:
   - Periodic tasks using Celery and Redis.
   - Email notifications for reservations.

4. **Caching**:
   - Redis-based caching for improved performance.

5. **Admin Panel**:
   - Manage users, reservations, and services.

---

## Static and Media Files

- **Static Files**:
  - URL: `/static/`
  - Directory: `static/`
  - Collected to: `staticfiles/`

- **Media Files**:
  - URL: `/media/`
  - Directory: `media/`

---

## Logging

The project uses `colorlog` for enhanced logging. Logs are displayed in the console with color-coded levels:
- **DEBUG**: Cyan
- **INFO**: Green
- **WARNING**: Yellow
- **ERROR**: Red
- **CRITICAL**: Bold Red

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.