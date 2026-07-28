from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from application.extensions import db, Base

# Junction table enabling the Many-to-Many relationship between tickets and mechanics
service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

# Junction table enabling the Many-to-Many relationship between tickets and inventory parts
service_ticket_inventory = db.Table(
    'service_ticket_inventory',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('inventory_id', db.ForeignKey('inventory.id'))
)


class Customer(Base):
    """A customer who brings vehicles in for service."""
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # One-to-Many: a customer can have multiple service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        back_populates='customer'
    )


class ServiceTicket(Base):
    """A single service job tied to a customer's vehicle."""
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    # Many-to-One: each ticket belongs to a single customer
    customer: Mapped['Customer'] = db.relationship(
        back_populates='service_tickets'
    )

    # Many-to-Many: a ticket can be assigned to multiple mechanics
    mechanics: Mapped[List['Mechanic']] = db.relationship(
        secondary=service_mechanics,
        back_populates='service_tickets'
    )

    # Many-to-Many: a ticket can require multiple inventory parts
    inventory_items: Mapped[List['Inventory']] = db.relationship(
        secondary=service_ticket_inventory,
        back_populates='service_tickets'
    )


class Mechanic(Base):
    """An employee who performs work on service tickets."""
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Many-to-Many: a mechanic can work on multiple tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        secondary=service_mechanics,
        back_populates='mechanics'
    )


class Inventory(Base):
    """A part that can be used on service tickets."""
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Many-to-Many: a part can be used on multiple tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        secondary=service_ticket_inventory,
        back_populates='inventory_items'
    )
