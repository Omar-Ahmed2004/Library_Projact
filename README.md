# Library Management System

A web-based Library Management System built with Django. The system allows librarians to manage books and members to borrow and return books.

## Features

* User authentication (Login / Logout)

* User roles:

  * Admin
  * Librarian
  * Member

* Book management:

  * Add books
  * Edit books
  * Delete books
  * View book details

* Categories and Authors

* Search books by:

  * Title
  * Author
  * Category
  * ISBN

* Filter books by category and author

* Pagination

* Borrow books

* Return books

* Track available copies

* Due dates

* Overdue loan detection

* Personal loan history

* Library dashboard

* Django Admin Panel

* Success, error, and warning messages

## Technologies

* Python
* Django
* SQLite
* HTML
* CSS
* Django ORM
* Django Authentication System

## Project Structure

```text
library_system/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── decorators.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
│
├── books/
│   ├── migrations/
│   ├── templates/
│   │   └── books/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
│
├── library_system/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── db.sqlite3
└── README.md
```

## Main Models

### Book

Stores information about books including:

* Title
* ISBN
* Publication year
* Total copies
* Available copies
* Category
* Author

### Loan

Tracks borrowing operations including:

* User
* Book
* Borrow date
* Due date
* Return status
* Return date

### Category

Stores book categories.

### Author

Stores book authors.

## User Roles

### Admin

Can access the Django Admin Panel and manage the system.

### Librarian

Can:

* Add books
* Edit books
* Delete books
* Manage library inventory

### Member

Can:

* View books
* Search and filter books
* Borrow books
* Return borrowed books
* View personal loans

## Installation

Clone the repository:

```bash
git clone https://github.com/Omar-Ahmed2004/Library_Projact.git
```

Move into the project directory:

```bash
cd Library_Projact
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Admin Panel

The Django Admin Panel is available at:

```text
http://127.0.0.1:8000/admin/
```

Use the superuser account created with:

```bash
python manage.py createsuperuser
```

## Future Improvements

Possible future improvements include:

* PostgreSQL database
* Environment variables
* REST API using Django REST Framework
* Automated tests
* Better UI design
* Deployment

## Author

Omar Ahmed

Computer Science Graduate

GitHub: https://github.com/Omar-Ahmed2004

