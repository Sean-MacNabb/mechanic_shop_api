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


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)