from application import create_app
from application.extensions import db
from application.models import Customer
from application.utils.util import encode_token
import unittest


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create a customer directly in the db so login/update/delete/
            # my-tickets tests have something to work against
            self.customer = Customer(
                name="Test User",
                email="test@email.com",
                phone="123-456-7890",
                password="test123"
            )
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id

        # Build a token for this customer to use on protected routes
        self.token = encode_token(self.customer_id)
        self.client = self.app.test_client()

    # ---------------- CREATE ----------------

    def test_create_customer(self):
        payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        self.assertEqual(response.json['email'], "jd@email.com")

    def test_create_customer_missing_field(self):
        # negative test: missing required "email" field
        payload = {
            "name": "John Doe",
            "phone": "555-123-4567",
            "password": "password123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_customer_duplicate_email(self):
        # negative test: email already used by the customer created in setUp
        payload = {
            "name": "Someone Else",
            "email": "test@email.com",
            "phone": "555-999-8888",
            "password": "password123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Email already associated with an account.")

    # ---------------- LOGIN ----------------

    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test123"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['message'], 'Successfully logged in')
        self.assertIn('auth_token', response.json)

    def test_login_invalid_credentials(self):
        # negative test: wrong password
        credentials = {
            "email": "test@email.com",
            "password": "wrong_password"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Invalid email or password')

    # ---------------- READ ----------------

    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_get_customer_by_id(self):
        response = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "test@email.com")

    def test_get_customer_not_found(self):
        # negative test: id that doesn't exist
        response = self.client.get('/customers/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Customer not found.")

    # ---------------- UPDATE (token required, no id in URL) ----------------

    def test_update_customer(self):
        payload = {"name": "Updated Name"}
        headers = {'Authorization': f"Bearer {self.token}"}
        response = self.client.put('/customers/', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")

    def test_update_customer_no_token(self):
        # negative test: no Authorization header
        payload = {"name": "Updated Name"}
        response = self.client.put('/customers/', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Token is missing!')

    # ---------------- DELETE (token required, no id in URL) ----------------

    def test_delete_customer(self):
        headers = {'Authorization': f"Bearer {self.token}"}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_no_token(self):
        # negative test: no Authorization header
        response = self.client.delete('/customers/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Token is missing!')

    # ---------------- MY TICKETS (token required) ----------------

    def test_my_tickets(self):
        headers = {'Authorization': f"Bearer {self.token}"}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  # no tickets created for this customer yet

    def test_my_tickets_no_token(self):
        # negative test: no Authorization header
        response = self.client.get('/customers/my-tickets')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Token is missing!')


if __name__ == '__main__':
    unittest.main()