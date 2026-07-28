from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from application.extensions import db
from application.models import Inventory
from application.blueprints.inventory import inventory_bp
from application.blueprints.inventory.schemas import inventory_schema, inventories_schema


# CREATE a new part
@inventory_bp.route("/", methods=['POST'])
def create_part():
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_part = Inventory(**part_data)
    db.session.add(new_part)
    db.session.commit()
    return inventory_schema.jsonify(new_part), 201


# READ all parts
@inventory_bp.route("/", methods=['GET'])
def get_parts():
    query = select(Inventory)
    parts = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(parts)


# READ a single part by id
@inventory_bp.route("/<int:part_id>", methods=['GET'])
def get_part(part_id):
    part = db.session.get(Inventory, part_id)

    if part:
        return inventory_schema.jsonify(part), 200
    return jsonify({"error": "Part not found."}), 404


# UPDATE a part by id
@inventory_bp.route("/<int:part_id>", methods=['PUT'])
def update_part(part_id):
    part = db.session.get(Inventory, part_id)

    if not part:
        return jsonify({"error": "Part not found."}), 404

    try:
        part_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in part_data.items():
        setattr(part, key, value)

    db.session.commit()
    return inventory_schema.jsonify(part), 200


# DELETE a part by id
@inventory_bp.route("/<int:part_id>", methods=['DELETE'])
def delete_part(part_id):
    part = db.session.get(Inventory, part_id)

    if not part:
        return jsonify({"error": "Part not found."}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part id: {part_id}, successfully deleted."}), 200