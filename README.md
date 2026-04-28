# **JWT AUTHENTICATION SYSTEM (FastAPI)**

**1\. DESCRIPTION**

This project is a backend authentication system build using FastAPI. It allows user to sign up, log in, and access protected routes using JWT- based authentication. The goal of this project is to deeply understand backend concepts like password hashing, token-based authentication and API design.

**2\. FEATURES**

- User Signup
- User Login
- Password Hashing (bcrypt)
- JWT Token Authentication
- Protected Routes
- Clean Project Structure

**3\. TECH STACK**

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- JWT(PyJWT)
- bcrypt

**4\. PROJECT STRUCTURE**

**app/**

- **main.py:** Entry Point
- **core/:** Config and security logic
- **db/:** Database connection and models
- **schemas/:** Requests/response models
- **api/routes/:** API endpoints
- **services/:** Business logic

**tests/:** Test files

**.env:** Environment variables

**requirements.txt:** Dependencies

**5\. API ENDPOINTS**

- **POST /signup:** Register user
- **POST /login:** Login user
- **GET /profile:** Protected routes

**6\. HOW TO RUN THE PROJECT**

- Clone the repo
- Create virtual environment
- Install dependencies
- Run server

**7\. FUTURE IMPROVEMENTS**

- Add refresh token
- Role-based authentication
- Deploy to cloud

**8\. LEARNING LOG**

- **Day1:** Set up FastAPI project and created basic API endpoint
- **Day2:** Designed project structure
