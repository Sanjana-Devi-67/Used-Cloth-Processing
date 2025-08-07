# Used Cloth Donation and Management System

A responsive Flask-based web application designed to streamline the management of used cloth donations. The platform enables users to donate clothes, track the real-time status of their donations, and provides an intuitive admin dashboard for efficient inventory control and distribution.

---

## Features

- **User Registration & Login**  
  Secure user authentication and session management via Flask-Login.

- **Donation Tracking**  
  Track the real-time status of donations from submission to distribution.

- **Admin Dashboard**  
  Admins can view, update, and delete donation records for effective inventory management.

- **Responsive UI**  
  Built with Bootstrap and Jinja2 for a clean and user-friendly interface.

- **Database Integration**  
  SQLite is used as the backend database, handled efficiently through SQLAlchemy ORM.

---

## Tech Stack

| Technology    | Usage                          |
|---------------|---------------------------------|
| Python        | Backend programming (Flask)     |
| Flask         | Web framework                   |
| SQLite        | Lightweight relational database |
| SQLAlchemy    | ORM for database interaction    |
| Bootstrap     | Responsive frontend styling     |
| Jinja2        | Templating engine               |
| HTML & CSS    | Web structure and styling       |

---

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

**Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cloth-donation-system.git
   cd cloth-donation-system
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
