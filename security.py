from flask import Blueprint, request, jsonify
from backend.db import get_db_connection
from backend.middleware.auth_middleware import token_required, role_required
import datetime

security_bp = Blueprint('security', __name__)

@security_bp.route('/visitors', methods=['GET'])
@token_required
@role_required([1, 3, 5]) 
def get_daily_visitors():
    """Returns today's visitors using the established Phase 1 view."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM view_daily_visitors")
        visitors = cursor.fetchall()
        return jsonify(visitors), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch daily visitors", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@security_bp.route('/visitors/log', methods=['POST'])
@token_required
@role_required([3]) 
def log_visitor_entry():
    """
    Records a visitor entry. Requires a transaction to safely handle both
    the 'visitors' table and the 'access_logs' table.
    """
    data = request.get_json()
    required = ['name', 'id_type', 'id_number', 'unit_id']
    if not all(k in data for k in required):
        return jsonify({"message": "Missing required fields"}), 400
        
    guard_id = request.user['user_id']
    gate_pass_code = data.get('gate_pass_code', f"GPC-{datetime.datetime.now().strftime('%H%M%S')}")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("START TRANSACTION")
        
       
        cursor.execute("SELECT id FROM visitors WHERE id_number = %s", (data['id_number'],))
        visitor = cursor.fetchone()
        
        if visitor:
            visitor_id = visitor['id']
        else:
            cursor.execute(
                "INSERT INTO visitors (name, id_type, id_number, contact_number) VALUES (%s, %s, %s, %s)",
                (data['name'], data['id_type'], data['id_number'], data.get('contact_number'))
            )
            visitor_id = cursor.lastrowid
            
       
        log_query = """
            INSERT INTO access_logs (visitor_id, unit_id, guard_id, exit_time, gate_pass_code)
            VALUES (%s, %s, %s, NULL, %s)
        """
        cursor.execute(log_query, (visitor_id, data['unit_id'], guard_id, gate_pass_code))
        new_log_id = cursor.lastrowid
        
        conn.commit()
        return jsonify({
            "message": "Visitor entry logged successfully",
            "log_id": new_log_id,
            "gate_pass_code": gate_pass_code
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Failed to log visitor", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@security_bp.route('/visitors/exit/<int:log_id>', methods=['PUT'])
@token_required
@role_required([3])
def log_visitor_exit(log_id):
    """Marks a visitor as exited by updating exit_time."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "UPDATE access_logs SET exit_time = CURRENT_TIMESTAMP WHERE id = %s AND exit_time IS NULL",
            (log_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Log not found or already exited"}), 404
        return jsonify({"message": "Visitor exit logged successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Failed to log exit", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
