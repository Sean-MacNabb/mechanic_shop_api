from application import create_app
from application.extensions import db
from application.models import Inventory
import unittest


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.part = Inventory(name="Brake Pad", price=45.99)
            db.session.add(self.part)
            db.session.commit()
            self.part_id = self.part.id

        self.client = self.app.test_client()

    # ---------------- CREATE ----------------

    def test_create_part(self):
        payload = {"name": "Oil Filter", "price": 12.50}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Oil Filter")

    def test_create_part_missing_field(self):
        # negative test: missing required "price" field
        payload = {"name": "Oil Filter"}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)

    # ---------------- READ ----------------

    def test_get_all_parts(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_part_by_id(self):
        response = self.client.get(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pad")

    def test_get_part_not_found(self):
        # negative test: id that doesn't exist
        response = self.client.get('/inventory/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Part not found.")

    # ---------------- UPDATE ----------------

    def test_update_part(self):
        payload = {"name": "Brake Pad (Ceramic)", "price": 52.99}
        response = self.client.put(f'/inventory/{self.part_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['price'], 52.99)

    def test_update_part_not_found(self):
        # negative test: id that doesn't exist
        payload = {"name": "Ghost Part", "price": 1.00}
        response = self.client.put('/inventory/99999', json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Part not found.")

    # ---------------- DELETE ----------------

    def test_delete_part(self):
        response = self.client.delete(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['message'],
            f"Part id: {self.part_id}, successfully deleted."
        )

    def test_delete_part_not_found(self):
        # negative test: id that doesn't exist
        response = self.client.delete('/inventory/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Part not found.")


if __name__ == '__main__':
    unittest.main()