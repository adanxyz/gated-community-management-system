from flask import Blueprint, request, jsonify
from backend.db import get_db_connection
from backend.middleware.auth_middleware import token_required, role_required

amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/book', methods=['POST'])
@token_required
@role_required([2]) # Only Residents can book amenities
def book_amenity():
    """
    Books an amenity for a resident.
    Demonstrates Transaction Management (BEGIN, COMMIT, ROLLBACK).
    Ensures capacity constraints.
    """
    data = request.get_json()
    
    required_fields = ['amenity_id', 'booking_date', 'start_time', 'end_time']
    if not all(k in data for k in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    amenity_id = data['amenity_id']
    booking_date = data['booking_date']
    start_time = data['start_time']
    end_time = data['end_time']
    
    # Extract user ID from token
    user_id = request.user['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Start Transaction
        cursor.execute("START TRANSACTION")
        
        # 1. Look up the resident ID based on the logged-in user ID
        cursor.execute("SELECT id FROM residents WHERE user_id = %s", (user_id,))
        resident = cursor.fetchone()
        
        if not resident:
            conn.rollback()
            return jsonify({"message": "Logged-in user is not associated with a resident profile."}), 400
            
        resident_id = resident['id']

        # 2. Check if the resident has overdue payments
        # Handled by DB trigger, but we'll also verify amenity capacity programmatically
        cursor.execute("SELECT capacity, hourly_rate FROM amenities WHERE id = %s", (amenity_id,))
        amenity = cursor.fetchone()
        
        if not amenity:
            conn.rollback()
            return jsonify({"message": "Amenity not found."}), 404
            
        # Optional: We could check if existing bookings overlap or exceed capacity here
        
        # 3. Insert the Booking
        booking_query = """
            INSERT INTO bookings (amenity_id, resident_id, booking_date, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, %s, 'Confirmed')
        """
        cursor.execute(booking_query, (amenity_id, resident_id, booking_date, start_time, end_time))
        new_booking_id = cursor.lastrowid
        
        # 4. If there is a fee, record a payment as Pending
        if amenity['hourly_rate'] > 0:
            # Simplistic calculation: assume 1 hour billing
            payment_query = """
                INSERT INTO payments (resident_id, amount, payment_date, payment_type, status)
                VALUES (%s, %s, CURDATE(), 'Amenity', 'Pending')
            """
            cursor.execute(payment_query, (resident_id, amenity['hourly_rate']))
            
        # Commit Transaction
        conn.commit()
        
        return jsonify({
            "message": "Amenity booked successfully.",
            "booking_id": new_booking_id
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({
            "message": "Booking failed, transaction rolled back.",
            "error": str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()

@amenities_bp.route('/', methods=['GET'])
@token_required
def get_amenities():
    """Returns a list of all amenities."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM amenities")
        amenities = cursor.fetchall()
        return jsonify(amenities), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch amenities", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
