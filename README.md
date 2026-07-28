# Mechanic Shop API

A RESTful API for managing a mechanic shop's customers, mechanics, service tickets, and parts inventory, built with Flask, SQLAlchemy, and Marshmallow using the Application Factory pattern.

## Features

- Full CRUD operations for Customers, Mechanics, Service Tickets, and Inventory parts
- One-to-Many relationship between Customers and Service Tickets
- Many-to-Many relationship between Service Tickets and Mechanics
- Many-to-Many relationship between Service Tickets and Inventory parts
- Token-based authentication (JWT) for customer login and protected routes
- Rate limiting on account creation to prevent abuse
- Response caching to reduce repeated database queries
- Pagination on the customer list endpoint
- Bulk add/remove of mechanics on a service ticket
- Endpoint ranking mechanics by number of tickets worked
- Request validation and serialization via Marshmallow schemas
- Modular blueprint structure for scalability
- Environment-based configuration (Development / Testing / Production)

## Tech Stack

- **Flask** – web framework
- **Flask-SQLAlchemy** – ORM for MySQL
- **Flask-Marshmallow** / **marshmallow-sqlalchemy** – serialization, deserialization, and validation
- **Flask-Limiter** – rate limiting
- **Flask-Caching** – response caching
- **python-jose** – JWT token encoding/decoding
- **MySQL** – database
- **python-dotenv** – environment variable management

## Project Structure

```
mechanic_shop/
├── application/
│   ├── __init__.py              # create_app() factory function
│   ├── extensions.py            # db, ma, limiter, and cache instances
│   ├── models.py                # Customer, ServiceTicket, Mechanic, Inventory models
│   ├── utils/
│   │   └── util.py              # encode_token() and token_required decorator
│   └── blueprints/
│       ├── customer/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── mechanic/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── service_ticket/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       └── inventory/
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
- **Service Ticket** ↔ **Inventory**: Many-to-Many (a ticket can require multiple parts, and a part can be used on multiple tickets), connected through a `service_ticket_inventory` junction table

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

| Method | Endpoint             | Auth Required | Description                          |
|--------|-----------------------|:---:|---------------------------------------|
| POST   | `/customers/`         |     | Create a new customer (rate limited) |
| POST   | `/customers/login`    |     | Log in with email/password, returns a token |
| GET    | `/customers/`         |     | Get all customers (paginated: `?page=&per_page=`) |
| GET    | `/customers/<id>`     |     | Get a specific customer              |
| GET    | `/customers/my-tickets` | ✅ | Get service tickets for the logged-in customer |
| PUT    | `/customers/`         | ✅ | Update the logged-in customer's own account (partial updates supported) |
| DELETE | `/customers/`         | ✅ | Delete the logged-in customer's own account |

### Mechanics — `/mechanics`

| Method | Endpoint                | Description                              |
|--------|--------------------------|-------------------------------------------|
| POST   | `/mechanics/`            | Create a new mechanic                    |
| GET    | `/mechanics/`            | Get all mechanics (cached 60s)           |
| GET    | `/mechanics/most-tickets`| Get mechanics ranked by tickets worked   |
| PUT    | `/mechanics/<id>`        | Update a mechanic (partial updates supported) |
| DELETE | `/mechanics/<id>`        | Delete a mechanic                        |

### Service Tickets — `/service-tickets`

| Method | Endpoint                                                      | Description                          |
|--------|------------------------------------------------------------------|----------------------------------------|
| POST   | `/service-tickets/`                                          | Create a new service ticket          |
| GET    | `/service-tickets/`                                          | Get all service tickets              |
| PUT    | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket        |
| PUT    | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket      |
| PUT    | `/service-tickets/<ticket_id>/edit`                          | Bulk add/remove mechanics via `add_ids` and `remove_ids` |
| PUT    | `/service-tickets/<ticket_id>/add-part/<part_id>`            | Add an inventory part to a ticket    |

### Inventory — `/inventory`

| Method | Endpoint          | Description             |
|--------|-------------------|--------------------------|
| POST   | `/inventory/`     | Create a new part       |
| GET    | `/inventory/`     | Get all parts            |
| GET    | `/inventory/<id>` | Get a specific part      |
| PUT    | `/inventory/<id>` | Update a part (partial updates supported) |
| DELETE | `/inventory/<id>` | Delete a part            |

## Authentication

Customers log in via `POST /customers/login` with an email and password, and receive a JWT valid for 1 hour. Protected routes require this token in the request header:

```
Authorization: Bearer <token>
```

## Testing

A Postman collection (`Mechanic_Shop_API.postman_collection.json`) is included with pre-built requests for every endpoint, organized by resource. Import it into Postman to test the API:

1. Open Postman
2. Click **Import**
3. Select `Mechanic_Shop_API.postman_collection.json`
4. Run **Login** first, then copy the returned `auth_token` into the collection's `auth_token` variable to use the protected routes

## Notes

- `db.create_all()` only creates tables that don't already exist — it will not overwrite or duplicate existing tables, and is safe to run on every app start.
- Model field changes made after tables already exist require either dropping/recreating tables or a migration tool (e.g. Flask-Migrate), since `create_all()` does not alter existing tables.
- The mechanic list cache (60 seconds) does not automatically invalidate on create/update/delete; changes may take up to 60 seconds to appear in `GET /mechanics/`.
