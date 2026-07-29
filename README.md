# Mechanic Shop API
 
**🚀 Live API:** https://mechanic-shop-api-v2de.onrender.com
**📄 Live API Docs:** https://mechanic-shop-api-v2de.onrender.com/api/docs/
 
A RESTful API for managing a mechanic shop's customers, mechanics, service tickets, and parts inventory, built with Flask, SQLAlchemy, and Marshmallow using the Application Factory pattern. Deployed on Render with a fully automated CI/CD pipeline via GitHub Actions.
 
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
- Interactive API documentation via Swagger UI
- Full automated test suite covering every endpoint (positive and negative cases)
- Modular blueprint structure for scalability
- Environment-based configuration (Development / Testing / Production)
- Deployed on Render (Web Service + managed PostgreSQL database)
- CI/CD pipeline via GitHub Actions: every push automatically builds the app, runs the full test suite, and — only if tests pass — deploys the latest code to production

## Tech Stack
 
- **Flask** – web framework
- **Flask-SQLAlchemy** – ORM for MySQL
- **Flask-Marshmallow** / **marshmallow-sqlalchemy** – serialization, deserialization, and validation
- **Flask-Limiter** – rate limiting
- **Flask-Caching** – response caching
- **python-jose** – JWT token encoding/decoding
- **flask-swagger-ui** – interactive API documentation
- **MySQL** – local development/testing database
- **PostgreSQL** – production database (hosted on Render)
- **python-dotenv** – environment variable management (local only)
- **unittest** – automated testing
- **gunicorn** – production WSGI server
- **psycopg2** – PostgreSQL database adapter
- **GitHub Actions** – CI/CD pipeline
- **Render** – cloud hosting for the API and database
## Project Structure
 
```
mechanic_shop/
├── application/
│   ├── __init__.py              # create_app() factory function
│   ├── extensions.py            # db, ma, limiter, and cache instances
│   ├── models.py                # Customer, ServiceTicket, Mechanic, Inventory models
│   ├── static/
│   │   └── swagger.yaml         # OpenAPI/Swagger documentation for all endpoints
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
├── tests/
│   ├── test_customer.py
│   ├── test_mechanic.py
│   ├── test_service_ticket.py
│   └── test_inventory.py
├── .github/
│   └── workflows/
│       └── main.yaml             # CI/CD pipeline: build -> test -> deploy
├── flask_app.py                  # entry point, runs create_app() with ProductionConfig
├── config.py                     # environment configuration classes (Dev/Testing/Production)
├── .env                          # local environment variables (not committed)
├── .gitignore
├── requirements.txt
└── Mechanic_Shop_API_v2.postman_collection.json
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
CREATE DATABASE mechanic_shop_test_db;
```
 
The second database is used exclusively by the automated test suite, so tests never touch real data.
 
### 5. Configure environment variables
 
Create a `.env` file in the project root:
 
```
DB_PASSWORD=your_mysql_password_here
```
 
### 6. Run the application locally
 
```bash
python flask_app.py
```
 
The API will be available at `http://127.0.0.1:5000` when run locally with `DevelopmentConfig`. Tables are created automatically on startup if they don't already exist.
 
> **Note:** A live version of this API is already deployed and publicly available — see the links at the top of this README. You don't need to run it locally to use it.
 
## Deployment
 
This API is deployed on [Render](https://render.com) as a Web Service, connected to a managed Render PostgreSQL database (separate from the local MySQL databases used for development/testing).
 
**Production setup:**
- `config.py` includes a `ProductionConfig` class that reads `SQLALCHEMY_DATABASE_URI` and other secrets from environment variables (set directly in Render's dashboard, not from a `.env` file)
- `flask_app.py` calls `create_app('config.ProductionConfig')` and is served in production via `gunicorn flask_app:app`
- `psycopg2` is used as the PostgreSQL driver in production (MySQL's `mysql-connector-python` is only used locally)
**Continuous Deployment:** Auto-Deploy is turned **off** on Render. Instead, deployment is fully controlled by the GitHub Actions pipeline described below — code only reaches production after it passes the automated test suite.
 
## CI/CD Pipeline
 
Every push to `main` triggers a GitHub Actions workflow (`.github/workflows/main.yaml`) with three sequential jobs:
 
1. **`build`** — checks out the code, sets up Python, and installs dependencies to confirm the project builds cleanly
2. **`test`** *(depends on `build`)* — spins up a temporary MySQL service container, runs the full `unittest` suite against it (`python -m unittest discover -s tests -p 'test_*.py'`), and fails the pipeline if any test fails
3. **`deploy`** *(depends on `test`)* — only runs if `test` passes; triggers a deploy on Render via [`johnbeynon/render-deploy-action`](https://github.com/johnbeynon/render-deploy-action), using the repo's `SERVICE_ID` and `RENDER_API_KEY` secrets
This means broken code can never reach production — a failing test blocks the deploy job entirely. You can watch any run under the repo's **Actions** tab.
 
**Required GitHub repository secrets** (Settings → Secrets and variables → Actions):
 
| Secret | Used by | Purpose |
|---|---|---|
| `DB_PASSWORD` | `test` job | Root password for the MySQL service container used to run tests |
| `SECRET_KEY` | `test` job | JWT signing key, so token-related tests can run |
| `SERVICE_ID` | `deploy` job | Identifies which Render Web Service to deploy |
| `RENDER_API_KEY` | `deploy` job | Authenticates the deploy request with Render |
 
## API Documentation
 
Interactive Swagger documentation:
 
- **Live:** https://mechanic-shop-api-v2de.onrender.com/api/docs/
- **Local:** `http://127.0.0.1:5000/api/docs/` (when running locally)
This includes every endpoint grouped by resource (Customers, Mechanics, Service Tickets, Inventory), with example request/response bodies and the ability to test routes directly from the browser using the "Try it out" feature — including against the live production API.
 
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
 
### Automated tests
 
A full `unittest` suite covers every endpoint, including negative cases (missing fields, duplicate emails, invalid login, missing/invalid tokens, and not-found lookups). Tests run against a dedicated `mechanic_shop_test_db` database, so they never touch real data — each test resets the database via `db.drop_all()` / `db.create_all()` before running.
 
Run the full suite:
 
```bash
python -m unittest discover tests
```
 
### Manual testing
 
A Postman collection (`Mechanic_Shop_API_v2.postman_collection.json`) is included with pre-built requests for every endpoint, organized by resource. Import it into Postman to test the API:
 
1. Open Postman
2. Click **Import**
3. Select `Mechanic_Shop_API_v2.postman_collection.json`
4. Run **Login** first, then copy the returned `auth_token` into the collection's `auth_token` variable to use the protected routes
Alternatively, use the Swagger UI at `/api/docs/` to test endpoints directly from the browser.
 
## Notes
 
- `db.create_all()` only creates tables that don't already exist — it will not overwrite or duplicate existing tables, and is safe to run on every app start.
- Model field changes made after tables already exist require either dropping/recreating tables or a migration tool (e.g. Flask-Migrate), since `create_all()` does not alter existing tables.
- The mechanic list cache (60 seconds) does not automatically invalidate on create/update/delete; changes may take up to 60 seconds to appear in `GET /mechanics/`.
 
