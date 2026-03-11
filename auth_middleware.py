import os
import jwt
from functools import wraps
from flask import request, jsonify

def get_secret_key():
    return os.getenv("JWT_SECRET", "super_secret_jwt_key_change_in_production")

def generate_token(user_id, username, role_id):
   
    payload = {
        "user_id": user_id,
        "username": username,
        "role_id": role_id
    }
    return jwt.encode(payload, get_secret_key(), algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
       
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing"}), 401
            
        try:
            data = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
           
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
            
        return f(*args, **kwargs)
    return decorated

def role_required(required_roles):
    """
    Middleware to ensure the user has one of the required roles.
    Assumes role_ids map to roles in DB: 
    1: Admin, 2: Resident, 3: Security, 4: Maintenance, 5: Manager
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not getattr(request, 'user', None):
                return jsonify({"message": "Authentication required"}), 401
                
            user_role = request.user.get('role_id')
            if user_role not in required_roles:
                return jsonify({"message": "Forbidden. You do not have the required role."}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
