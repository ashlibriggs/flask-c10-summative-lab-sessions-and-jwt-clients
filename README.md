# Productivity App API

## Overview

This project is a Flask REST API for a productivity application that allows users to create accounts, log in, manage tasks, and securely access their own data using session-based authentication.

Users can:

* Sign up for an account
* Log in and log out
* Persist authentication using Flask sessions
* Create tasks
* View all of their tasks
* View a specific task
* Update existing tasks
* Delete tasks
* Access paginated task results

---

## Features

* Flask REST API
* SQLAlchemy ORM
* Flask-Migrate database migrations
* Flask-Bcrypt password hashing
* Session authentication
* User model with secure password storage
* Full CRUD functionality for tasks
* Pagination support
* Error handling and validations

---

## Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Bcrypt
* SQLite
* SQLAlchemy ORM
* Pipenv

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

Install dependencies:

```bash
pipenv install
pipenv shell
```

Initialize the database:

```bash
flask db upgrade
```

Seed the database:

```bash
python seed.py
```

Run the server:

```bash
python app.py
```

The API will run at:

```bash
http://localhost:5555
```

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| POST   | /signup        | Register a new user   |
| POST   | /login         | Log in a user         |
| GET    | /check_session | Verify active session |
| DELETE | /logout        | Log out current user  |

### Tasks

| Method | Endpoint    | Description                         |
| ------ | ----------- | ----------------------------------- |
| GET    | /tasks      | Retrieve all tasks for current user |
| POST   | /tasks      | Create a new task                   |
| GET    | /tasks/<id> | Retrieve a single task              |
| PATCH  | /tasks/<id> | Update a task                       |
| DELETE | /tasks/<id> | Delete a task                       |

---

## Example Request

Create a new task:

```bash
curl -b cookies.txt -X POST http://localhost:5555/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Finish Capstone","description":"Prepare for final project"}'
```

---

## Database Models

### User

* id
* username
* password_hash

### Task

* id
* title
* description
* completed
* user_id

Relationships:

* A User has many Tasks.
* A Task belongs to one User.

---

## Author

Ashli Briggs

Software Engineering student transitioning from entrepreneurship and digital operations into full-stack software engineering with a focus on building user-centered applications and AI-enabled products.
