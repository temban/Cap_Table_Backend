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
git clone https://github.com/your-repo/cap-table-backend.git
cd cap-table-backend
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
DATABASE_URL="postgresql://postgres:admin@localhost:5432/cap_table_db"
SECRET_KEY="your-secret-key"
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
```

### **5. Initialize the Database**  
```bash
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
| `/api/token/` | POST | Login (JWT) | Public |
| `/api/shareholders/` | GET | List shareholders | Admin |
| `/api/issuances/` | POST | Issue shares | Admin |
| `/api/issuances/{id}/certificate` | GET | Download PDF | Shareholder/Admin |

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

detailed
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
1. **Audit Trail** – Log all critical actions (e.g., share issuance).  
2. **Async Tasks** – Use Celery for background email sending.  
3. **Enhanced Security** – Rate limiting, OAuth2 scopes.  
4. **Frontend Integration** – Connect with a React dashboard.  

---

## **📜 License**  
MIT License – Free for use and modification.  

---

## **📞 Contact**  
For questions or feedback:  
📧 **Email**: tembanblaise1@gmail.com  
🌐 **GitHub**: [your-github](https://github.com/temban)  

---

**🎉 Happy Coding!** 🚀