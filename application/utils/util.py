import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from jose import jwt
import jose

# Falls back to a hardcoded value if SECRET_KEY isn't set as an environment
# variable — needed for local dev/testing and CI, where no such env var
# exists. In production (Render), the real SECRET_KEY env var overrides this.
SECRET_KEY = os.environ.get('SECRET_KEY') or "a super secret, secret key"


# Builds a JWT containing the customer's id, valid for 1 hour
def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


# Protects a route by requiring a valid Bearer token, passes customer_id to the wrapped function
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split(" ")
            # expects format "Bearer <token>", so guard against malformed headers
            if len(auth_header) == 2:
                token = auth_header[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = data['sub']
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(customer_id, *args, **kwargs)

    return decorated