# Mechanic Shop API

A RESTful API for managing a mechanic shop's customers, mechanics, and service tickets, built with Flask, SQLAlchemy, and Marshmallow using the Application Factory pattern.

## Requirements

- flask
- flask-sqlalchemy
- flask-marshmallow
- marshmallow-sqlalchemy
- mysql-connector-python
- python-dotenv

## Features

- Full CRUD operations for Customers, Mechanics, and Service Tickets
- One-to-Many relationship between Customers and Service Tickets
- Many-to-Many relationship between Service Tickets and Mechanics
- Request validation and serialization via Marshmallow schemas
- Modular blueprint structure for scalability
- Environment-based configuration (Development / Testing / Production)

## Tech Stack

- **Flask** – web framework
- **Flask-SQLAlchemy** – ORM for MySQL
- **Flask-Marshmallow** / **marshmallow-sqlalchemy** – serialization, deserialization, and validation
- **MySQL** – database
- **python-dotenv** – environment variable management

## Project Structure

```
mechanic_shop/
├── application/
│   ├── __init__.py              # create_app() factory function
│   ├── extensions.py            # db and ma instances
│   ├── models.py                # Customer, ServiceTicket, Mechanic models
│   └── blueprints/
│       ├── customer/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── mechanic/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       └── service_ticket/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
├── app.py                       # entry point, runs create_app()
├── config.py                    # environment configuration classes
├── .env                         # local environment variables (not committed)
├── .gitignore
├── requirements.txt
└── Mechanic_Shop_API.postman_collection.json
```

## Entity-Relationship Overview

- **Customer** → **Service Ticket**: One-to-Many (a customer can have multiple service tickets)
- **Service Ticket** ↔ **Mechanic**: Many-to-Many (a ticket can have multiple mechanics assigned, and a mechanic can work on multiple tickets), connected through a `service_mechanics` junction table

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd mechanic_shop
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your database

In MySQL Workbench or the MySQL CLI:

```sql
CREATE DATABASE mechanic_shop_db;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```
DB_PASSWORD=your_mysql_password_here
```

### 6. Run the application

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`. Tables are created automatically on startup if they don't already exist.

## API Endpoints

### Customers — `/customers`

| Method | Endpoint          | Description             |
|--------|-------------------|--------------------------|
| POST   | `/customers/`     | Create a new customer   |
| GET    | `/customers/`     | Get all customers       |
| GET    | `/customers/<id>` | Get a specific customer |
| PUT    | `/customers/<id>` | Update a customer       |
| DELETE | `/customers/<id>` | Delete a customer       |

### Mechanics — `/mechanics`

| Method | Endpoint          | Description              |
|--------|-------------------|---------------------------|
| POST   | `/mechanics/`     | Create a new mechanic    |
| GET    | `/mechanics/`     | Get all mechanics        |
| PUT    | `/mechanics/<id>` | Update a mechanic        |
| DELETE | `/mechanics/<id>` | Delete a mechanic        |

### Service Tickets — `/service-tickets`

| Method | Endpoint                                                | Description                          |
|--------|----------------------------------------------------------|---------------------------------------|
| POST   | `/service-tickets/`                                     | Create a new service ticket          |
| GET    | `/service-tickets/`                                     | Get all service tickets              |
| PUT    | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket   |
| PUT    | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket |

## Testing

A Postman collection (`Mechanic_Shop_API.postman_collection.json`) is included with pre-built requests for every endpoint. Import it into Postman to test the API:

1. Open Postman
2. Click **Import**
3. Select `Mechanic_Shop_API.postman_collection.json`
4. Run requests in this suggested order: Create Customer → Create Mechanic → Create Service Ticket → Assign Mechanic to Ticket → Get All Service Tickets