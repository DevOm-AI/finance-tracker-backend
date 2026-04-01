## 📊 Personal Finance Tracking System (Backend)
Built as a technical assignment to demonstrate proficiency in Python, FastAPI, and Relational Database Design. This system provides a robust API for managing financial records with built-in analytics and Role-Based Access Control (RBAC).

## 🚀 Tech Stack
Language: Python 3.9+

Framework: FastAPI (Chosen for its high performance, Pydantic validation, and auto-generated OpenAPI docs).

Database: SQLite (Chosen for its simplicity, zero-configuration, and ease of portability).

ORM: SQLAlchemy (Used to abstract database logic and ensure maintainability).

## 🏗️ System Architecture & Design Choices
1. Layered Architecture
The project follows a "Separation of Concerns" pattern to keep the code clean and testable:

models.py: Defines the physical data structure in SQLite.

schemas.py: Handles data validation and serialization (Pydantic).

database.py: Manages the connection pool and session lifecycle.

main.py: Houses the API routes and business logic.

2. Role-Based Access Control (RBAC)
To meet the "User Handling" requirement without the overhead of complex OAuth2 flows, I implemented a Header-based Permission System:

Viewer: Read-only access to transaction history.

Analyst: Access to filtered history + Financial Analytics & Summaries.

Admin: Full CRUD permissions (Create, Update, Delete).

3. Efficient Analytics
Instead of processing data in Python memory, I utilized SQL Aggregations (func.sum and group_by) to calculate balances and category-wise breakdowns. This ensures the system remains fast even as the database grows.

## 🛠️ Features Implemented
[x] Full CRUD: Create, Read, Update, and Delete financial entries.

[x] Financial Analytics: Real-time calculation of Total Income, Expense, and Balance.

[x] Data Filtering: Search records by Category or Type (Income/Expense).

[x] Security: Role-based endpoint protection.

[x] CSV Export: (Bonus) Export all financial data to a CSV file for external reporting.

[x] Auto-Docs: Integrated Swagger UI for instant testing.

## 🚦 How to Run the Project
1. Clone & Setup Environment
Bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Launch the Server
Bash
uvicorn app.main:app --reload
4. Access the API
Interactive API Docs (Swagger): http://127.0.0.1:8000/docs

Root Endpoint: http://127.0.0.1:8000/

## 📝 Assumptions Made
Authentication: For the scope of this assignment, user identification is handled via the X-User-Role request header.

Currency: All financial amounts are treated as a single uniform currency (e.g., INR).

Database: The SQLite file (finance.db) is automatically generated upon the first application startup.