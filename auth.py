from flask import Blueprint, request, jsonify
from models import User, RefreshToken
from database import db
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from app import limiter

import bcrypt
import jwt
import re
import os

from datetime import datetime, timedelta

from middleware import token_required

auth = Blueprint("auth", __name__)

def validate_password(password):

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'

    return re.match(pattern, password)


def generate_access_token(user):

    payload = {
        "id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }

    return jwt.encode(
        payload,
        os.getenv("ACCESS_SECRET"),
        algorithm="HS256"
    )


def generate_refresh_token(user):

    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    return jwt.encode(
        payload,
        os.getenv("REFRESH_SECRET"),
        algorithm="HS256"
    )


@auth.route("/register", methods=["POST"])
def register():

    data = request.json

    password = data["password"]

    if not validate_password(password):

        return jsonify({
            "message": "Weak password"
        }), 400

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(10)
    )

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password.decode("utf-8"),
        role=data["role"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created"
    })


@auth.route("/login", methods=["POST"])
@limiter.limit("5 per 15 minutes")
def login():

    data = request.json

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:

        return jsonify({
            "message": "User not found"
        }), 400

    valid_password = bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user.password.encode("utf-8")
    )

    if not valid_password:

        return jsonify({
            "message": "Wrong password"
        }), 400

    access_token = generate_access_token(user)

    refresh_token = generate_refresh_token(user)

    token_row = RefreshToken(
        token=refresh_token,
        user_id=user.id
    )

    db.session.add(token_row)

    db.session.commit()

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

@auth.route("/logout", methods=["POST"])
def logout():

    data = request.json

    refresh_token = data.get("refresh_token")

    if not refresh_token:

        return jsonify({
            "message": "Refresh token required"
        }), 400

    token = RefreshToken.query.filter_by(
        token=refresh_token
    ).first()

    if not token:

        return jsonify({
            "message": "Token not found"
        }), 404

    db.session.delete(token)

    db.session.commit()

    return jsonify({
        "message": "Logged out successfully"
    })


@auth.route("/refresh", methods=["POST"])
def refresh():

    data = request.json

    refresh_token = data["refresh_token"]

    token_exists = RefreshToken.query.filter_by(
        token=refresh_token
    ).first()

    if not token_exists:

        return jsonify({
            "message": "Invalid refresh token"
        }), 403

    try:

        payload = jwt.decode(
            refresh_token,
            os.getenv("REFRESH_SECRET"),
            algorithms=["HS256"]
        )

        user = User.query.get(payload["id"])

        access_token = generate_access_token(user)

        return jsonify({
            "access_token": access_token
        })

    except:

        return jsonify({
            "message": "Token expired"
        }), 403


@auth.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):

    data = request.json

    current_user.bio = data.get("bio")

    current_user.avatar_url = data.get("avatar_url")

    db.session.commit()

    return jsonify({
        "message": "Profile updated"
    })


@auth.route("/change-password", methods=["POST"])
@token_required
def change_password(current_user):

    data = request.json

    old_password = data["old_password"]

    new_password = data["new_password"]

    valid_password = bcrypt.checkpw(
        old_password.encode("utf-8"),
        current_user.password.encode("utf-8")
    )

    if not valid_password:

        return jsonify({
            "message": "Wrong old password"
        }), 400

    if not validate_password(new_password):

        return jsonify({
            "message": "Weak password"
        }), 400

    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt(10)
    )

    current_user.password = hashed_password.decode("utf-8")

    db.session.commit()

    return jsonify({
        "message": "Password changed"
    })