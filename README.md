# FastAPI Project

A brief description of your FastAPI project, what it does, and why it's useful.

## About

This FastAPI project is a simple web API built using **FastAPI** for building web applications and services. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

The project implements a user authentication system, supports CRUD operations, and provides an authentication token using OAuth2 and JWT.

---

## Features

- User registration and login
- JWT authentication and token management
- Built-in validation using Pydantic models
- Swagger UI documentation for easy API interaction
- MySQL integration for persistence

---

## Installation

To get started with this FastAPI project, follow the steps below to set up the project on your local machine.

### Prerequisites

- Python 3.7+ (recommended: Python 3.10 or later)
- `pip` (Python's package installer)
- MySQL or SQLite database (depending on your configuration)

### Step 1: Clone the Repository

Clone this repository to your local machine:

```
git clone https://github.com/Dhvanil0594/fast-api-demo.git
cd fast-api-demo
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

It’s recommended to create a virtual environment to manage dependencies:

```
python3 -m venv venv
```

Activate the virtual environment:

Linux/macOS:

```
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required dependencies using pip:

```
pip install -r requirements.txt
```

## Usage

### Step 1: Set Up the Database

You may need to set up the database (MySQL or SQLite, depending on your configuration). You can use Alembic to handle database migrations.

To initialize the database schema, run the following command (make sure you’ve configured `alembic.ini` to match your database settings):

```
alembic upgrade head
```

### Step 2: Start the FastAPI Server

Once dependencies are installed and the database is set up, you can start the development server using Uvicorn:

```
uvicorn app.main:app --reload
```

### Step 3: Access Swagger UI

Once the server is running, you can visit the Swagger UI documentation for your API at:

[http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

The FastAPI project includes the following main API endpoints:

### 1. **POST /api/v1/user-auth/signup**

Register a new user. This endpoint expects the following payload:

```
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123"
}
```

### 2. **POST /api/v1/user-auth/login**

Log in an existing user and get a JWT access token:

```
{
  "username": "user123",
  "password": "password123"
}
```
