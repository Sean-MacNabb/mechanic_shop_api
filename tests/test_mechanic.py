from application import create_app
from application.extensions import db
from application.models import Mechanic
import unittest


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.mechanic = Mechanic(
                name="Alex Torres",
                email="alex@shop.com",
                phone="555-000-1111",
                salary=55000.00
            )
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id

        self.client = self.app.test_client()

    # ---------------- CREATE ----------------

    def test_create_mechanic(self):
        payload = {
            "name": "Sam Rivera",
            "email": "sam@shop.com",
            "phone": "555-222-3333",
            "salary": 60000.00
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Sam Rivera")

    def test_create_mechanic_missing_field(self):
        # negative test: missing required "salary" field
        payload = {
            "name": "Sam Rivera",
            "email": "sam@shop.com",
            "phone": "555-222-3333"
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_mechanic_duplicate_email(self):
        # negative test: email already used by the mechanic created in setUp
        payload = {
            "name": "Someone Else",
            "email": "alex@shop.com",
            "phone": "555-999-8888",
            "salary": 50000.00
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Email already associated with an account.")

    # ---------------- READ ----------------

    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_mechanics_most_tickets(self):
        response = self.client.get('/mechanics/most-tickets')
        self.assertEqual(response.status_code, 200)

    # ---------------- UPDATE ----------------

    def test_update_mechanic(self):
        payload = {"salary": 65000.00}
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['salary'], 65000.00)

    def test_update_mechanic_not_found(self):
        # negative test: id that doesn't exist
        payload = {"salary": 65000.00}
        response = self.client.put('/mechanics/99999', json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Mechanic not found.")

    # ---------------- DELETE ----------------

    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['message'],
            f"Mechanic id: {self.mechanic_id}, successfully deleted."
        )

    def test_delete_mechanic_not_found(self):
        # negative test: id that doesn't exist
        response = self.client.delete('/mechanics/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Mechanic not found.")


if __name__ == '__main__':
    unittest.main()