from flask import Blueprint, jsonify
from middleware import token_required, role_required
from models import User

admin = Blueprint("admin", __name__)

@admin.route("/users", methods=["GET"])
@token_required
@role_required("admin")
def get_users(current_user):

    users = User.query.all()

    result = []

    for user in users:

        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

    return jsonify(result)