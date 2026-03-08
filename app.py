from flask import Flask, jsonify
from backend.routes.auth import auth_bp
from backend.routes.amenities import amenities_bp
from backend.routes.admin import admin_bp
from backend.routes.resident import resident_bp
from backend.routes.security import security_bp
from backend.db import init_db_pool

app = Flask(__name__)


init_db_pool()


app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
app.register_blueprint(resident_bp, url_prefix='/api/v1/resident')
app.register_blueprint(security_bp, url_prefix='/api/v1/security')

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the Gated Community Management API v1",
        "status": "Healthy"
    }), 200

if __name__ == '__main__':
   
    app.run(host='0.0.0.0', port=5000, debug=True)
