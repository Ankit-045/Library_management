# 📚 Library Management System

[**Live Demo**](https://library-management-1-rms3.onrender.com/)

A full-stack web application for managing a small library. It features a FastAPI backend for handling data and logic, and a Streamlit frontend for a user-friendly, interactive interface.

## ✨ Features

*   **User Management**:
    *   User signup and login.
    *   JWT-based authentication for secure API access.
    *   Role-based access control distinguishing between `student` and `incharge` users.

*   **Student Portal**:
    *   View a list of all books and their availability status.
    *   Request to borrow an available book.
    *   View personal booking history with statuses (pending, approved, rejected, returned).

*   **Incharge (Admin) Portal**:
    *   View and manage all user booking requests.
    *   Approve or reject pending book requests.
    *   Mark approved books as "returned" once they are back in the library.
    *   Add new books to the library collection.
    *   Delete books from the library.

## 🛠️ Technologies Used

*   **Backend**:
    *   FastAPI: For building the robust and fast RESTful API.
    *   SQLAlchemy: For ORM (Object Relational Mapping) to interact with the database.
    *   Pydantic: For data validation and settings management.
    *   python-jose: For handling JWTs (JSON Web Tokens).
    *   passlib: For secure password hashing (using Argon2).
    *   Uvicorn: As the ASGI server for FastAPI.

*   **Frontend**:
    *   Streamlit: For creating the interactive web application.

*   **Database**:
    *   SQLite: As the lightweight, file-based database.

## 📂 Project Structure

```
├── .
├── auth.py             # Authentication logic (JWT, password hashing)
├── database.py         # Database engine and session setup
├── main.py             # FastAPI application entry point
├── models.py           # SQLAlchemy ORM models
├── requirements.txt    # Project dependencies
├── routers/            # Directory for API route modules
│   ├── books.py
│   ├── bookings.py
│   └── user.py
├── schemas.py          # Pydantic schemas for data validation
└── streamlit_app.py    # Streamlit frontend application
```

## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd library-management-system
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## 🏃 Running the Application

You need to run the backend and frontend servers in separate terminals.

### 1. Start the FastAPI Backend

Navigate to the project's root directory and run:

```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`. You can explore the interactive API documentation at `http://localhost:8000/docs`.

### 2. Start the Streamlit Frontend

In a new terminal, run:

```bash
streamlit run streamlit_app.py
```

The web application will open in your browser, usually at `http://localhost:8501`.

## 🧑‍💻 How to Use

1.  **Create an 'Incharge' User**: The first thing you should do is sign up as an `incharge`. This role is required to add books and manage the library.
2.  **Add Books**: Log in as the `incharge` user and navigate to the "Manage Books" tab to add new books to the library.
3.  **Student Usage**: Sign up or log in with a `student` account.
    *   In the "All Books" tab, you can see the list of available books and request to borrow them.
    *   In the "My Bookings" tab, you can track the status of your book requests.
4.  **Manage Bookings**: The `incharge` user can view all booking requests in the "Manage Bookings" tab and approve, reject, or mark them as returned.

---