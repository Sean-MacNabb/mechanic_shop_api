from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from application.extensions import db, limiter
from application.models import Customer, ServiceTicket
from application.blueprints.customer import customer_bp
from application.blueprints.customer.schemas import customer_schema, customers_schema, login_schema
from application.blueprints.service_ticket.schemas import service_tickets_schema
from application.utils.util import encode_token, token_required


# CREATE a new customer
@customer_bp.route("/", methods=['POST'])
@limiter.limit("5 per hour")  # limits spam/abuse of account creation
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check whether this email is already tied to an existing customer
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


# LOGIN with email and password, returns a token
@customer_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password:
        auth_token = encode_token(customer.id)
        return jsonify({
            "status": "success",
            "message": "Successfully logged in",
            "auth_token": auth_token
        }), 200
    return jsonify({"message": "Invalid email or password"}), 401


# READ all customers, supports ?page= and ?per_page= for pagination
@customer_bp.route("/", methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = select(Customer)
    customers = db.paginate(query, page=page, per_page=per_page)

    return customers_schema.jsonify(customers.items)


# READ a single customer by id
@customer_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404


# READ service tickets belonging to the logged-in customer
@customer_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200


# UPDATE the logged-in customer's own account
@customer_bp.route("/", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# DELETE the logged-in customer's own account
@customer_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer id: {customer_id}, successfully deleted."}), 200