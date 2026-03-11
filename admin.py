from flask import Blueprint, jsonify
from backend.db import get_db_connection
from backend.middleware.auth_middleware import token_required, role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/overview', methods=['GET'])
@token_required
@role_required([1, 5]) 
def get_system_overview():
    """
    Returns an overview of the system specifically for administrative roles.
    Demonstrates Role-Based Access Control and view utilization.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
       
        cursor.execute("SELECT * FROM view_active_bookings LIMIT 10")
        active_bookings = cursor.fetchall()
        
        # Get pending dues
        cursor.execute("SELECT * FROM view_resident_dues WHERE total_pending > 0 LIMIT 10")
        resident_dues = cursor.fetchall()

        return jsonify({
            "message": "System Overview retrieved successfully",
            "active_bookings": active_bookings,
            "resident_dues": resident_dues
        }), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch overview", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/users', methods=['GET'])
@token_required
@role_required([1]) 
def get_all_users():
    """Returns all users in the system."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, username, email, phone, role_id FROM users")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch users", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@role_required([1])
def delete_user(user_id):
    """Deletes a user from the system."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Failed to delete user", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/units', methods=['GET', 'POST'])
@token_required
@role_required([1, 5]) 
def manage_units():
    """Returns all units or creates a new one."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT * FROM units")
            units = cursor.fetchall()
            return jsonify(units), 200
            
        elif request.method == 'POST':
            data = request.get_json()
            required = ['unit_number', 'block', 'unit_type', 'square_feet']
            if not all(k in data for k in required):
                return jsonify({"message": "Missing fields"}), 400
            
            cursor.execute(
                "INSERT INTO units (unit_number, block, unit_type, square_feet) VALUES (%s, %s, %s, %s)",
                (data['unit_number'], data['block'], data['unit_type'], data['square_feet'])
            )
            conn.commit()
            return jsonify({"message": "Unit created successfully", "unit_id": cursor.lastrowid}), 201
    except Exception as e:
        if request.method == 'POST': conn.rollback()
        return jsonify({"message": "Failed to process units", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/staff', methods=['GET'])
@token_required
@role_required([1, 5])
def get_staff_allocations():
    """Returns staff assignments."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT s.id, u.username, u.email, u.phone, s.department, s.employee_id 
            FROM staff s
            JOIN users u ON s.user_id = u.id
        """
        cursor.execute(query)
        staff = cursor.fetchall()
        return jsonify(staff), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch staff", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/complaints', methods=['GET'])
@token_required
@role_required([1, 4, 5]) 
def get_all_complaints():
    """Returns all complaints lodged by residents."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT c.id, c.title, c.description, c.priority, c.status, c.created_at, u.unit_number 
            FROM complaints c
            JOIN residents r ON c.resident_id = r.id
            JOIN units u ON r.unit_id = u.id
            ORDER BY c.created_at DESC
        """
        cursor.execute(query)
        complaints = cursor.fetchall()
        return jsonify(complaints), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch complaints", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/payments', methods=['GET'])
@token_required
@role_required([1, 5]) 
def get_all_payments():
    """Returns all payments and rent statuses cross-referenced with resident units."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT p.id, u.username, un.unit_number, p.amount, p.payment_date, p.payment_type, p.status 
            FROM payments p
            JOIN residents r ON p.resident_id = r.id
            JOIN users u ON r.user_id = u.id
            JOIN units un ON r.unit_id = un.id
            ORDER BY p.payment_date DESC, p.status
        """
        cursor.execute(query)
        payments = cursor.fetchall()
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch payments", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
