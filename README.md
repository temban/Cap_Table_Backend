Here's a comprehensive `README.md` with a table of contents and detailed instructions for setting up, running, and testing your FastAPI backend:

```markdown
# Cap Table Management System - Backend

A FastAPI backend for managing company capitalization tables, shareholders, and share issuances with PDF certificate generation.

## Table of Contents
1. [Features](#features)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Setup & Installation](#setup--installation)
5. [Running the Application](#running-the-application)
6. [API Documentation](#api-documentation)
7. [Testing](#testing)
8. [Database Migrations](#database-migrations)
9. [Docker Deployment](#docker-deployment)
10. [Project Structure](#project-structure)
11. [Environment Variables](#environment-variables)
12. [Troubleshooting](#troubleshooting)

---

## Features
- **JWT Authentication**: Secure login/refresh endpoints
- **Role-Based Access**: Admin vs. shareholder permissions
- **Shareholder Management**: CRUD operations for shareholders
- **Share Issuance**: Issue shares with PDF certificate generation
- **Ownership Visualization**: Endpoint for pie chart data
- **Email Notifications**: SMTP integration for share issuance alerts
- **Unit & Integration Tests**: 85%+ test coverage

## Technologies
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL
- **PDF Generation**: ReportLab
- **Email**: SMTP (Gmail compatible)
- **Testing**: Pytest
- **Containerization**: Docker

---

## Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Docker (optional)
- Git

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Cap_Table_Backend.git
cd Cap_Table_Backend
```

### 2. Set up virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment
- **Linux/MacOS**:
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Database setup
1. Create a PostgreSQL database named `cap_table_db`
2. Update `.env` with your credentials:
   ```ini
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/cap_table_db
   ```

---

## Running the Application
```bash
# Make run.sh executable (Linux/Mac)
chmod +x run.sh

# Start the application
./run.sh
```
The server will run at `http://localhost:8000`

---

## API Documentation
Access interactive docs after running the server:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Testing

### Run all tests
```bash
pytest tests/ -v
```

### Test categories
| Command | Description |
|---------|-------------|
| `pytest tests/unit/` | Unit tests (services, utils) |
| `pytest tests/integration/` | API endpoint tests |
| `pytest --cov=app tests/` | Test coverage report |

### Key Test Cases
- Authentication flow (login, refresh, JWT validation)
- Shareholder CRUD operations
- Share issuance with PDF generation
- Role-based access control

---

## Database Migrations
```bash
# Create new migration (after model changes)
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

---

## Docker Deployment
1. Build and start containers:
   ```bash
   docker-compose up --build
   ```
2. Access at `http://localhost:8000`

---
## Project Structure
```
Cap_Table_Backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── issuance_controller.py
│   │   ├── shareholder_controller.py
│   │   └── user_controller.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── session.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── issuance_model.py
│   │   ├── shareholder_model.py
│   │   └── user_model.py
│   │
│   ├── routes/
│   │   └── api.py
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── issuance_schema.py
│   │   ├── shareholder_schema.py
│   │   └── user_schema.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── issuance_service.py
│   │   ├── shareholder_service.py
│   │   └── user_service.py
│   │
│   ├── utils/
│   │   ├── email_utils.py
│   │   ├── openapi_utils.py
│   │   └── pdf_utils.py
│   │
│   └── main.py
│
├── tests/
│   ├── integration/
│   │   ├── test_auth.py
│   │   ├── test_issuances.py
│   │   ├── test_shareholders.py
│   │   └── test_users.py
│   │
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   ├── test_issuance_service.py
│   │   ├── test_shareholder_service.py
│   │   └── conftest.py
│
├── venv/
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── run.sh
```

---

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://postgres:admin@localhost:5432/cap_table_db` |
| `SECRET_KEY` | JWT signing key | Random string |
| `SMTP_USER` | Email service username | - |
| `SMTP_PASSWORD` | Email service password | - |

---

## Troubleshooting
**Issue**: Database connection errors  
**Fix**: Verify PostgreSQL is running and credentials in `.env` match your DB setup

**Issue**: Missing dependencies  
**Fix**: Run `pip install -r requirements.txt` and check Python version (3.10+ required)

**Issue**: Migration conflicts  
**Fix**: Delete `alembic/versions/` and regenerate migrations
```

### Key Notes for Submission:
1. **Video Walkthrough**: Highlight:
   - Database initialization
   - Admin/shareholder login flow
   - Share issuance with PDF demo
   - Test execution

2. **AI Tools Used**: Mention if you used Copilot/Cursor for:
   - Boilerplate code generation
   - Test case suggestions
   - Documentation templates

3. **Future Improvements**:
   - Async email delivery (Celery/RQ)
   - Redis caching for frequent queries
   - WebSocket notifications

This README provides comprehensive guidance while showcasing your architectural decisions and attention to detail.