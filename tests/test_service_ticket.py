from application import create_app
from application.extensions import db
from application.models import Customer, Mechanic, ServiceTicket, Inventory
import unittest


class TestServiceTicket(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Test Customer",
                email="customer@email.com",
                phone="555-000-0000",
                password="test123"
            )
            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@email.com",
                phone="555-111-1111",
                salary=55000.00
            )
            self.part = Inventory(name="Brake Pad", price=45.99)

            db.session.add_all([self.customer, self.mechanic, self.part])
            db.session.commit()

            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id
            self.part_id = self.part.id

            # An existing ticket to test assign/remove/edit/add-part against
            self.ticket = ServiceTicket(
                VIN="1HGCM82633A004352",
                service_date="2026-07-27",
                service_desc="Oil change",
                customer_id=self.customer_id
            )
            db.session.add(self.ticket)
            db.session.commit()
            self.ticket_id = self.ticket.id

        self.client = self.app.test_client()

    # ---------------- CREATE ----------------

    def test_create_service_ticket(self):
        payload = {
            "VIN": "2FTRX18W1XCA12345",
            "service_date": "2026-07-28",
            "service_desc": "Tire rotation",
            "customer_id": self.customer_id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_desc'], "Tire rotation")

    def test_create_service_ticket_missing_field(self):
        # negative test: missing required "VIN" field
        payload = {
            "service_date": "2026-07-28",
            "service_desc": "Tire rotation",
            "customer_id": self.customer_id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    # ---------------- READ ----------------

    def test_get_all_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    # ---------------- ASSIGN / REMOVE MECHANIC ----------------

    def test_assign_mechanic_to_ticket(self):
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 200)
        mechanic_ids = [m['id'] for m in response.json['mechanics']]
        self.assertIn(self.mechanic_id, mechanic_ids)

    def test_assign_mechanic_already_assigned(self):
        # negative test: assigning the same mechanic twice
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Mechanic is already assigned to this ticket.")

    def test_remove_mechanic_from_ticket(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 200)
        mechanic_ids = [m['id'] for m in response.json['mechanics']]
        self.assertNotIn(self.mechanic_id, mechanic_ids)

    def test_remove_mechanic_not_assigned(self):
        # negative test: removing a mechanic that was never assigned
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Mechanic is not assigned to this ticket.")

    # ---------------- BULK EDIT MECHANICS ----------------

    def test_edit_mechanics_bulk(self):
        payload = {"add_ids": [self.mechanic_id], "remove_ids": []}
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit', json=payload)
        self.assertEqual(response.status_code, 200)
        mechanic_ids = [m['id'] for m in response.json['mechanics']]
        self.assertIn(self.mechanic_id, mechanic_ids)

    # ---------------- ADD PART ----------------

    def test_add_part_to_ticket(self):
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}'
        )
        self.assertEqual(response.status_code, 200)
        part_ids = [p['id'] for p in response.json['inventory_items']]
        self.assertIn(self.part_id, part_ids)

    def test_add_part_already_added(self):
        # negative test: adding the same part twice
        self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Part is already added to this ticket.")


if __name__ == '__main__':
    unittest.main()