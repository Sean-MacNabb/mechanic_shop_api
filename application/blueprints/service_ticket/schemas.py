from application.extensions import ma
from application.models import ServiceTicket


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        # include_fk makes customer_id available for load/dump, since it's
        # a foreign key column and excluded by default
        include_fk = True
        # include_relationships makes the mechanics list visible when we
        # serialize a ticket, so assigned mechanics actually show up in responses
        include_relationships = True

    # Limit the nested mechanic data to just id and name, so we don't dump
    # every field (and avoid circular nesting back into service_tickets)
    mechanics = ma.Nested('MechanicSchema', many=True, only=('id', 'name'))

    # dump_only means parts show in output but aren't required/loaded on input
    inventory_items = ma.Nested('InventorySchema', many=True, only=('id', 'name', 'price'), dump_only=True)

    # dump_only means this field is only used when serializing output (GET),
    # never required or accepted on input (POST/PUT) — fixes a bug where
    # creating a ticket failed because Marshmallow expected a full nested
    # customer object instead of just customer_id
    customer = ma.Nested('CustomerSchema', only=('id', 'name'), dump_only=True)


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
