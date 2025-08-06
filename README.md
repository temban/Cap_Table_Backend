# **Cap Table Management System - Backend (FastAPI)**  

A **FastAPI** backend for managing a company's capitalization table (Cap Table), including shareholder management, share issuance, and certificate generation.  

---

## **📋 Table of Contents**  
1. [Features](#-features)  
2. [Technologies](#-technologies)  
3. [Prerequisites](#-prerequisites)  
4. [Setup & Installation](#-setup--installation)  
5. [Running the Application](#-running-the-application)  
6. [Running Tests](#-running-tests)  
7. [API Documentation](#-api-documentation)  
8. [Project Structure](#-project-structure)  
9. [Future Improvements](#-future-improvements)  
10. [License](#-license)  

---

## **✨ Features**  
✅ **Authentication & Authorization**  
- JWT-based login (`/api/token/`)  
- Role-based access (Admin & Shareholder)  

✅ **Shareholder Management**  
- Admin can create, update, and deactivate shareholders  
- View total shares per shareholder  

✅ **Share Issuance**  
- Issue shares to shareholders  
- Generate PDF certificates (`/api/issuances/{id}/certificate`)  
- Email notifications (SMTP)  

✅ **Data Visualization**  
- Ownership distribution endpoint (`/api/issuances/distribution`)  

✅ **Testing**  
- Unit & integration tests  

✅ **Bonus Features**  
- Email notifications  
- Advanced validation (e.g., no negative shares)  

---

## **🛠 Technologies**  
- **Backend**: FastAPI (Python)  
- **Database**: PostgreSQL  
- **Authentication**: JWT  
- **PDF Generation**: ReportLab  
- **Email**: SMTP (Gmail)  
- **Testing**: Pytest  
- **Containerization**: Docker  

---

## **📦 Prerequisites**  
Before running the project, ensure you have:  
- **Python 3.9+**  
- **PostgreSQL** (running locally or in Docker)  
- **Git** (for cloning the repo)  
- **Pip** (for dependencies)  

Optional:  
- **Docker** (if running in a container)  

---

## **⚙ Setup & Installation**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/temban/Cap_Table_Backend.git
cd Cap_Table_Backend
```

### **2. Set Up a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**  
Create a `.env` file (or modify `run.sh`):  
```env

DATABASE_URL=postgresql://user:password@localhost:port/bd_name
SECRET_KEY=secret_key
ALGORITHM=algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP_HOST=smtp.gmail.com
SMTP_PORT=port
SMTP_USER=your-email@gmail.com
SMTP_PASS=password
SMTP_FROM=your-email@gmail.com
COMPANY_NAME=company_name
ENVIRONMENT=development
```

### **5. Initialize the Database**  
```bash
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
alembic stamp head
       or
python -m alembic upgrade head
python -m app.db.init_db
```

---

## **🚀 Running the Application**  
### **Option 1: Using `run.sh` (Linux/Mac)**
```bash
chmod +x run.sh  # Make executable
./run.sh         # Starts the server
```
- Runs migrations  
- Seeds initial data (admin & shareholder)  
- Starts FastAPI on `http://0.0.0.0:8000`  

### **Option 2: Manual Start**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Access Swagger UI: `http://localhost:8000/docs`  

### **Option 3: Docker (Recommended for Production)**
```bash
docker-compose up --build
```
- Starts PostgreSQL & FastAPI in containers  

---

## **🧪 Running Tests**  
### **1. Unit Tests**  
```bash
pytest tests/unit -v
```
Tests:  
- Authentication  
- Shareholder & Issuance services  

### **2. Integration Tests**  
```bash
pytest tests/integration -v
```
Tests:  
- API endpoints  
- Database interactions  

### **3. Test Coverage Report**  
```bash
pytest --cov=app tests/
```
Generates a coverage report in the terminal.  

---

## **📖 API Documentation**  
- **Swagger UI**: `http://localhost:8000/docs`  
- **Redoc**: `http://localhost:8000/redoc`  

### **Key Endpoints**  

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/token/` | POST | Login (JWT) - Returns access & refresh tokens | Public |
| `/api/token/refresh` | POST | Refresh access token using refresh token | Authenticated |
| `/api/shareholders/` | GET | List all shareholders with total shares (Dashboard view) | Admin |
| `/api/shareholders/` | POST | Create new shareholder (Name, Email) | Admin |
| `/api/shareholders/{id}` | GET | Get shareholder details | Admin |
| `/api/shareholders/{id}` | PUT | Update shareholder information | Admin |
| `/api/shareholders/{id}` | DELETE | Deactivate shareholder | Admin |
| `/api/issuances/` | GET | List all issuances (Admin) or only own (Shareholder) | Authenticated |
| `/api/issuances/` | POST | Create new share issuance | Admin |
| `/api/issuances/distribution` | GET | Get ownership distribution data for pie chart | Admin |
| `/api/issuances/{id}/certificate` | GET | Generate and download PDF share certificate | Owner/Admin |
| `/api/me` | GET | Get current user profile and shares (Shareholder dashboard) | Authenticated |

### User Story Mapping:
**Admin Features:**
- ✅ Login → `/api/token/` (POST)
- ✅ List shareholders → `/api/shareholders/` (GET)
- ✅ Ownership visualization → `/api/issuances/distribution` (GET)
- ✅ Add shareholder → `/api/shareholders/` (POST)
- ✅ Issue shares → `/api/issuances/` (POST)
- ✅ Generate certificate → `/api/issuances/{id}/certificate` (GET)

**Shareholder Features:**
- ✅ Login → `/api/token/` (POST)
- ✅ Personal dashboard → `/api/me` (GET)
- ✅ View issuances → `/api/issuances/` (GET)
- ✅ Download certificates → `/api/issuances/{id}/certificate` (GET)

This table now:
1. Covers all API endpoints from the technical requirements
2. Maps directly to each user story
3. Specifies access control (Public/Admin/Shareholder)
4. Includes both authentication endpoints and business logic endpoints
5. Shows all CRUD operations for shareholders and issuances
---

## **🗂 Project Structure**  
```plaintext
Cap_Table_Backend/
├── app/                 # Core application
│   ├── controllers/     # API routes
│   ├── core/            # Config & security
│   ├── db/              # Database setup
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic models
│   ├── services/        # Business logic
│   ├── utils/           # Helpers (PDF, email)
│   └── main.py          # FastAPI app
├── tests/               # Unit & integration tests
├── alembic/             # Database migrations
├── .env                 # Environment variables
├── docker-compose.yml   # Docker setup
└── README.md            # Project docs


Detailed Project Structure

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

## **🔮 Future Improvements**  
1. **Realtime Updates** – Implement WebSocket notifications for instant share price changes and issuance alerts.  
2. **Dynamic Equity Modeling** – Add cap table simulations to forecast dilution impacts before issuing new shares.  
3. **Automated Valuation** – Integrate with financial APIs to auto-calculate share prices based on company KPIs.  

Each delivers direct business value:  
- **Realtime** → Faster decision-making  
- **Modeling** → Prevent equity missteps  
- **Valuation** → Data-driven pricing

---

## **📜 License**  
MIT License – Free for use and modification.  

---

## **📞 Contact**  
For questions or feedback:  
📧 **Email**: tembanblaise1@gmail.com  
🌐 **GitHub**: [Temban Blaise](https://github.com/temban)  

---

**🎉 Happy Coding!** 🚀