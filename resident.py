from flask import Blueprint, request, jsonify
from backend.db import get_db_connection
from backend.middleware.auth_middleware import token_required, role_required

resident_bp = Blueprint('resident', __name__)

@resident_bp.route('/unit', methods=['GET'])
@token_required
@role_required([2])
def get_own_unit():
    """Returns details about the resident's unit."""
    user_id = request.user['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT u.*, r.residency_status, r.move_in_date 
            FROM residents r
            JOIN units u ON r.unit_id = u.id
            WHERE r.user_id = %s
        """
        cursor.execute(query, (user_id,))
        unit_details = cursor.fetchone()
        
        if not unit_details:
            return jsonify({"message": "Resident profile not found"}), 404
            
        return jsonify(unit_details), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch unit details", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@resident_bp.route('/fees', methods=['GET'])
@token_required
@role_required([2])
def get_fees():
    """Returns the resident's payment history and pending dues."""
    user_id = request.user['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM residents WHERE user_id = %s", (user_id,))
        resident = cursor.fetchone()
        if not resident: return jsonify({"message": "Not a resident"}), 404
        
        cursor.execute("SELECT * FROM payments WHERE resident_id = %s ORDER BY payment_date DESC", (resident['id'],))
        payments = cursor.fetchall()
        
        return jsonify({"payments": payments}), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch fees", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@resident_bp.route('/pay', methods=['POST'])
@token_required
@role_required([2])
def pay_fee():
    """Simulates paying a specific pending fee."""
    data = request.get_json()
    if 'payment_id' not in data:
        return jsonify({"message": "payment_id required"}), 400
        
    payment_id = data['payment_id']
    user_id = request.user['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("START TRANSACTION")
        
        
        cursor.execute("""
            SELECT p.id, p.status FROM payments p
            JOIN residents r ON p.resident_id = r.id
            WHERE p.id = %s AND r.user_id = %s
        """, (payment_id, user_id))
        
        payment = cursor.fetchone()
        if not payment:
            conn.rollback()
            return jsonify({"message": "Payment not found or unauthorized"}), 404
            
        if payment['status'] == 'Paid':
            conn.rollback()
            return jsonify({"message": "Payment is already marked as Paid"}), 400
            
        
        cursor.execute("UPDATE payments SET status = 'Paid' WHERE id = %s", (payment_id,))
        conn.commit()
        
        return jsonify({"message": "Payment successful"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Payment failed", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@resident_bp.route('/complaints', methods=['GET', 'POST'])
@token_required
@role_required([2])
def manage_complaints():
    """Views or lists complaints for the resident."""
    user_id = request.user['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM residents WHERE user_id = %s", (user_id,))
        resident = cursor.fetchone()
        if not resident: return jsonify({"message": "Not a resident"}), 404
        resident_id = resident['id']
        
        if request.method == 'GET':
            cursor.execute("SELECT * FROM complaints WHERE resident_id = %s ORDER BY created_at DESC", (resident_id,))
            complaints = cursor.fetchall()
            return jsonify(complaints), 200
            
        elif request.method == 'POST':
            data = request.get_json()
            if 'title' not in data or 'description' not in data:
                return jsonify({"message": "Missing title or description"}), 400
                
            priority = data.get('priority', 'Medium')
            
            cursor.execute("START TRANSACTION")
            insert_query = """
                INSERT INTO complaints (resident_id, title, description, priority, status)
                VALUES (%s, %s, %s, %s, 'Open')
            """
            cursor.execute(insert_query, (resident_id, data['title'], data['description'], priority))
            conn.commit()
            
            return jsonify({
                "message": "Complaint lodged successfully",
                "complaint_id": cursor.lastrowid
            }), 201
            
    except Exception as e:
        if request.method == 'POST': conn.rollback()
        return jsonify({"message": "Failed to manage complaints", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
