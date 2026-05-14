import jwt
from functools import wraps
from flask import request, jsonify
from models import User
import os

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        auth_header = request.headers.get("Authorization")

        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({
                "message": "Token missing"
            }), 401

        try:

            data = jwt.decode(
                token,
                os.getenv("ACCESS_SECRET"),
                algorithms=["HS256"]
            )

            current_user = User.query.get(data["id"])

        except:
            return jsonify({
                "message": "Invalid token"
            }), 403

        return f(current_user, *args, **kwargs)

    return decorated


def role_required(role):

    def wrapper(f):

        @wraps(f)
        def decorated(current_user, *args, **kwargs):

            if current_user.role != role:

                return jsonify({
                    "message": "Access denied"
                }), 403

            return f(current_user, *args, **kwargs)

        return decorated

    return wrapper