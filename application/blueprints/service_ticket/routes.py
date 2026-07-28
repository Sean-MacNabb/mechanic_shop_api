from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from application.extensions import db
from application.models import ServiceTicket, Mechanic, Inventory
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


# EDIT a ticket's mechanics in bulk using add_ids and remove_ids
@service_ticket_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    add_ids = request.json.get('add_ids', [])
    remove_ids = request.json.get('remove_ids', [])

    # Look up and remove each mechanic by id
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    # Look up and append each mechanic by id
    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# ADD a single inventory part to a service ticket
@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=['PUT'])
def add_part(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not part:
        return jsonify({"error": "Part not found."}), 404

    if part in ticket.inventory_items:
        return jsonify({"error": "Part is already added to this ticket."}), 400

    ticket.inventory_items.append(part)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200
