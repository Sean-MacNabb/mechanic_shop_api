from application.extensions import ma
from application.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    # load_only means password is accepted on input but never returned in responses
    password = ma.String(load_only=True)

    class Meta:
        model = Customer


# LoginSchema only exposes email and password, used for the login route
class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ('email', 'password')


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()
