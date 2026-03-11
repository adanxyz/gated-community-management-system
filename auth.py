from flask import Blueprint, request, jsonify
import bcrypt
from backend.db import get_db_connection
from backend.middleware.auth_middleware import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a user and maps them to a resident profile.
    Demonstrates Transaction Management (BEGIN, COMMIT, ROLLBACK).
    """
    data = request.get_json()
    
    # Basic validation
    required_fields = ['username', 'password', 'email', 'unit_id', 'residency_status']
    if not all(k in data for k in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    username = data['username']
    password = data['password']
    email = data['email']
    phone = data.get('phone', None)
    unit_id = data['unit_id']
    residency_status = data['residency_status']
    move_in_date = data.get('move_in_date', None)

    # Hash the password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Start Transaction
        cursor.execute("START TRANSACTION")
        # Explicit BEGIN can also be used depending on MySQL config, START TRANSACTION is standard.

        # 2. Insert into users table
        # We assign role_id 2 for Resident by default in this flow.
        user_insert_query = """
            INSERT INTO users (username, password_hash, email, phone, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(user_insert_query, (username, password_hash, email, phone, 2))
        
        # Get the new user's ID
        new_user_id = cursor.lastrowid

        # 3. Insert into residents table
        resident_insert_query = """
            INSERT INTO residents (user_id, unit_id, residency_status, move_in_date)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(resident_insert_query, (new_user_id, unit_id, residency_status, move_in_date))

        # 4. Commit Transaction
        conn.commit()
        
        return jsonify({
            "message": "User and Resident profiles created successfully",
            "user_id": new_user_id
        }), 201

    except Exception as e:
        # 5. Rollback on any failure
        conn.rollback()
        return jsonify({
            "message": "Registration failed, transaction rolled back.",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and returns a JWT.
    """
    data = request.get_json()
    
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Username and password required"}), 400

    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, username, password_hash, role_id FROM users WHERE username = %s", (username,))
        user_record = cursor.fetchone()
        
        if not user_record:
            return jsonify({"message": "Invalid username or password"}), 401
            
        is_valid = False
        try:
            # Try to check against a proper bcrypt hash
            if bcrypt.checkpw(password.encode('utf-8'), user_record['password_hash'].encode('utf-8')):
                is_valid = True
        except ValueError:
            # Fallback for plain-text seed data from Phase 1 (e.g., 'h_admin')
            # In a production environment, this fallback should NOT exist.
            if password == user_record['password_hash']:
                is_valid = True

        if is_valid:
            # Successful login
            token = generate_token(user_record['id'], user_record['username'], user_record['role_id'])
            return jsonify({
                "message": "Login successful",
                "token": token
            }), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
            
    except Exception as e:
        return jsonify({"message": "An error occurred during login.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

