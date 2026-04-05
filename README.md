# Gated Community Management System (Phase 3)

## 1. Project Overview
A comprehensive Gated Community Management System dealing with managing units, residents, staff, security, and amenities. It solves the decentralized community management problem by offering unified, role-based access for CRUD operations, finance tracking, and real-time security handling.
**Team Members:** [Fatima Muaaz(BSCS24029), Adan Zubair (BSCS24011)]
**Group Number:** [26]

## 2. Tech Stack
- **Frontend Framework:** Streamlit (Python 3.10+)
- **Backend Framework:** Flask (Python)
- **Database:** MySQL
- **Authentication Method:** PyJWT (JSON Web Tokens) with `bcrypt` password hashing.
- **Third-Party Libraries:** `pandas` (for data-handling/UI tables), `requests` (for REST API communication), `mysql-connector-python` (for database drivers).

## 3. System Architecture
The application is robustly designed on a standard Client-Server architecture:
1. **Frontend (Streamlit):** Maintains session state (JWT tokens) and conditionally renders Role-Based dashboards while seamlessly issuing HTTP requests to our remote backend.
2. **Backend (Flask):** Serves the secure REST API, tightly enforces Role-Based Access Control logic on the endpoints via custom decorators, and coordinates explicit database transactions. 
3. **Database (MySQL):** The ultimate persistence layer maintaining referential integrity across interconnected tables (via foreign keys) and utilizing dynamic views and triggers for streamlined performance.

*(**Note on Directory Deviation:** Per phase instructions, deviations are acceptable if cleanly documented. Because we utilized Streamlit instead of React/Node.js, the `frontend/` directory does not contain `src/`, `public/`, or `package.json`, but rather relies exclusively on `app.py` and `requirements.txt`. Additionally, due to adopting raw optimized SQL queries rather than an ORM, we heavily utilize `backend/db.py` rather than maintaining a standard `models/` filesystem hierarchical layout.)*

## 4. UI Examples

1. **Admin Analytics Dashboard:**  `![Admin Analytics Dashboard](media/Admin_overview_page.png)` 
   *Working & Why required:* Provides administrators with dynamic charts of pending resident dues. Essential for complex feature requirement satisfaction (Visualizations).
2. **Resident Due Payments:** `![Resident Due Payments](media/Resident_dashboard_page.png)`
   *Working & Why required:* Allows residents to see their pending dues and pay them on time.
3. **Security Log Tracker:** `![Security Logger](media/Security_dashboard_page.png)`
   *Working & Why required:* Enables the security team to actively log entries and exits. Required to demonstrate our distinct Role-Based UI parameters. 

## 5. Setup & Installation
### Prerequisites
- Python 3.10+
- MySQL Server

### Step-by-Step Commands
**1. Initialise the Database:**
Ensure MySQL is actively running on your machine, then populate our schemas and mock data manually:
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql
```

**2. Configure `.env` files:**
- In your root folder, copy `.env.example` to `.env`. Populate it like so: `DB_HOST=localhost`, `DB_USER=root`, `DB_PASSWORD=your_password`, `DB_NAME=gated_community_db`, and `JWT_SECRET=supersecret123`.
- In the `frontend/` folder, copy `.env.example` to `.env`. Ensure it reads: `BACKEND_URL=http://localhost:5000/api/v1`.

**3. Start the Backend Server:**
Open a terminal targeting the root directory.
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r backend/requirements.txt
python -m backend.app
```
   
**4. Start the Frontend Dev Server:**
Open a completely separate (second) terminal targeting the root directory.
```bash
.\venv\Scripts\activate
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

## 6. User Roles
- **Admin (Role_ID: 1):** Full system access. Create units, view global analytics, view complaints natively, delete users.
  - *Testing Credential:* `admin01` / `h_admin`
- **Resident (Role_ID: 2):** Access to their personal assigned unit features, fee payments, and amenity bookings.
  - *Testing Credential:* `john_doe` / `password123` (or `res001` / `h_res`)
- **Security (Role_ID: 3):** Manage incoming and outgoing visitor logs safely.
  - *Testing Credential:* `guard01` / `h_guard`
  
*(Note: `Maintenance` and `Manager` exist natively in the data model, however, their UI flows structurally merge into the Admin's viewing privileges for this immediate phase).*

## 7. Feature Walkthrough
- **User Authentication:** (All Roles). Securely login and receive an API JWT token mapping rigidly to `/api/v1/auth/login`.
- **System Overview Analytics:** (Admin). Access interactive Bar Charts combining complex datasets dynamically from `view_active_bookings` & `view_resident_dues` mapped to `/api/v1/admin/overview`.
- **Fee Payment Processing:** (Resident). Securely checks out pending dues, explicitly triggering a DB transaction, mapped to `/api/v1/resident/pay`.
- **Visitor Entry Tracking:** (Security). Rapidly processes arriving visitor IDs by appending dynamic entry strings to `access_logs`, mapped to `/api/v1/security/visitors/log`.

## 8. Transaction Scenarios
**Scenario: Amenity Booking**
- **Triggers:** Resident confirms an amenity booking.
- **Operations Bundled Atomically:** Evaluates scheduling constraints -> Inserts booking query securely into `bookings` -> Checks if conditionally applying fee payment -> Evaluates `Overdue` conditional constraints.
- **Rollback Causes:** If the resident has an overdue payment, a MySQL Trigger forcefully raises a `45000` SQL state constraint. This immediately disrupts and fails the `INSERT`, fundamentally causing `backend/routes/amenities.py` to intercept the Exception and successfully execute `conn.rollback()`.
- **Relevant Endpoint:** API `POST /api/v1/amenities/book` inside `backend/routes/amenities.py`

## 9. ACID Compliance
| Property | Implementation strategy |
|---|---|
| **Atomicity** | Python `mysql-connector` uses explicitly declared `conn.commit()` and `conn.rollback()` ensuring if one query inside an endpoint sequence fails, absolutely all preceding operations rigidly revert. |
| **Consistency** | Database natively features extensive `FOREIGN KEY` constraints (e.g. `ON DELETE CASCADE`), `UNIQUE` constraints (e.g. `id_number`), and `CHECK` logic limitations (`amount > 0`). |
| **Isolation** | Flask organically handles highly independent concurrent request threads transmitting over localized database Cursor sessions efficiently avoiding `Dirty Reads`. |
| **Durability** | Backed fully by the industrial InnoDB MySQL engine preserving the explicit state permanently deep into memory logs strictly post `commit()`. |

## 10. Indexing & Performance
- **Indexes Created:** 
  - `idx_users_username` exclusively on `users(username)`: Added purposefully to optimize critical authentication lookup speeds exponentially during high traffic login spikes.
  - `idx_logs_entry` exclusively on `access_logs(entry_time)`: Sped up overarching range queries utilized fundamentally in the complex local visitor statistics view.
  - `idx_payments_status` explicitly on `payments(status)`: Vastly improved nested aggregate data filtering mapping exclusively for Admin pending dues tracking visualizers.
- **Performance Summary:** According strictly to our exported `performance.sql` benchmarks, successfully running nested aggregate queries heavily relying on `payments` transitioned from a painful full table scan (~10.2 ms) efficiently down to a highly optimized index lookup (~1.1 ms) routinely upon filtering directly by status.

## 11. API Reference
| Method | Route | Auth Required | Purpose |
|---|---|---|---|
| POST | `/api/v1/auth/register` | No | Registers Users & Residents Atomically |
| POST | `/api/v1/auth/login` | No | Issues Standard Session JWT Tokens |
| GET | `/api/v1/admin/overview` | Admin | Serves Dashboard Visual Analytics Resource Data |
| POST | `/api/v1/resident/pay` | Resident | Settles outstanding open balances directly via atomic transaction |
| POST | `/api/v1/amenities/book` | Resident | Process highly complex atomic amenity scheduling insertion |
| POST | `/api/v1/security/visitors/log` | Security | Pushes new Visitor entry generation logically |

*(See `docs/swagger.yaml` actively for complete, highly detailed structural specification parameters).*

## 12. Known Issues & Limitations
- **Maintenance Dashboards:** The `Maintenance` and `Manager` roles exist structurally solid within our database schema explicitly for overarching RBAC enforcement; however, their highly dedicated frontend interactive views were deferred explicitly exclusively due to Phase 3 MVP boundary constraints. The Admin structurally oversees actionable `Maintenance/Complaints` natively.
- **Overlapping Bookings Constraints:** Amenity capacity checks inherently allow for superficially successful insertions structurally across highly overlapping strict time constraints as deep time-checking internal logic algorithms run currently superficial limits.
- **Mock Hashing Protocols:** Test data mockups loaded from local `seed.sql` intentionally bypass bcrypt standard hashing upon database import (e.g. `h_admin`), whereas entirely true live accounts functionally created gracefully within the active frontend fully utilize universally secure `bcrypt` logic.
