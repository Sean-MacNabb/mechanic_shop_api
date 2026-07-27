from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from application.extensions import db
from application.models import ServiceTicket, Mechanic
from application.blueprints.service_ticket import service_ticket_bp
from application.blueprints.service_ticket.schemas import service_ticket_schema, service_tickets_schema


# CREATE a new service ticket
@service_ticket_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201


# ASSIGN a mechanic to a service ticket
@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    # Avoid adding the same mechanic to the ticket twice
    if mechanic in ticket.mechanics:
        return jsonify({"error": "Mechanic is already assigned to this ticket."}), 400

    # Since mechanics is a relationship list, we can just append to it
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# REMOVE a mechanic from a service ticket
@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this ticket."}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# READ all service tickets
@service_ticket_bp.route("/", methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets)
