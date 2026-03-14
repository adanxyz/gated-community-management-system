# Backend Explanation Document

**Course Phase 2 Submission**: Gated Community Management API

---

## 1. System Architecture & Request Lifecycle

Our application uses a minimalistic **Flask API** serving as the presentation layer, connecting directly to a local MySQL Database utilizing `mysql-connector-python`. We specifically elected to strictly use Python code without any Object Relational Mappers (ORM) like SQLAlchemy to fulfill project guidelines and guarantee performance visibility over every query execute.

### Request Lifecycle
1. **Client Request:** An HTTP request hits our Flask server (`/api/v1/...`).
2. **Middleware (Security & Auth):** Before the corresponding route handler is called, the request passes through custom decorators (`@token_required`, `@role_required`). These check the `Authorization` headers for a valid JWT and examine the decoded `role_id` against the endpoint's strict Role-Based Access Control list.
3. **Route Logic & DB Parsing:** The authenticated route handler initiates a connection from the Database Connection Pool, dynamically binding endpoint arguments to raw SQL strings utilizing *parameterized inputs*—shielding the server against SQL Injection.
4. **Transaction Resolution:** For modifying queries (`INSERT`, `UPDATE`), an explicit `START TRANSACTION` command is fired. The Python code attempts consecutive queries. If successful, `conn.commit()` is called. If Python catches any downstream errors (such as MySQL constraint failures or trigger panics), the `except` block catches it and fires `conn.rollback()`.
5. **Response Return:** Finally, Python closes the SQL cursor and returns a formalized JSON response alongside appropriate semantic HTTP Content Codes (e.g., `201 Created` or `401 Unauthorized`).

---

## 2. Authentication Flow & RBAC Enforcement

The system implements stateless JSON Web Token (JWT) authentication merged directly with persistent Role Based Access Control (RBAC).

*   **Registration Process:** When a user is inserted heavily salted passwords are generated locally by python’s `bcrypt` module. Only `.hashpw()` outputs are stored into the Database's `password_hash` column.
*   **Login Flow:** Upon correct `/login` credential submission (matching `bcrypt.checkpw()`), the backend encodes a JWT containing standard payloads (`user_id`, `role_id`) signed symmetrically utilizing Python `PyJWT` with the `HS256` hashing algorithm against a protected secret.
*   **RBAC Enforcement:** When a client accesses a protected amenity viewing endpoint, the request headers are sliced by the `@token_required` decorator. If decoding proceeds successfully—proving server authorship—the inner `@role_required` decorator cross references the injected Token payload's `role_id` against a hardcoded list mapping directly to the DB's `.roles` table elements (e.g., *[1]* for Admin, *[2]* for Residents).

---

## 3. Transaction Flows & Rollback Conditions

Our project utilizes True Backend Transaction logic utilizing standard explicit multi-step `BEGIN / COMMIT / ROLLBACK` commands directly wrapped around `mysql-connector-python`. Actual real-time database locks are successfully employed by the RDBMS engine. 

### Scenario 1: New Resident and User Registration (`/auth/register`)
This is arguably the most vulnerable endpoint in the system. A new Resident profile requires *both* a newly created row in `users` and a bound mapping referencing that generic auto-incremental user ID inside the `residents` table bridging them toward a concrete property `unit_id`.
*   **Implementation Flow:** The connection opens and fires `START TRANSACTION`. First, a row is placed inside `users` storing the `bcrypt` hashed password. Python sequentially pulls `cursor.lastrowid` and proceeds immediately to run a subsequent `INSERT INTO residents`. If everything succeeds, the backend triggers `conn.commit()`.
*   **Rollback condition:** If the provided user attempts to reserve `email` strings that uniquely violate MySQL constraints, or mapped `residency_status` constraint enum bindings are faulty, the exception triggers the script to fire `conn.rollback()`, ensuring no detached `users` ghosts exist without a mapped unit.

### Scenario 2: Amenity Booking Management (`/amenities/book`)
*   **Implementation Flow:** Start transaction. The `user_id` inside the validated JSON web token queries the `residents` table to fetch their authoritative local Resident mapped ID. Once found, an insert runs against `bookings` claiming the requested `amenity_id` for given temporal strings. Upon successful reservation logic, if the Amenity specifies a non-zero fee via `hourly_rate`, the very next line fires an `INSERT INTO payments (...)  'Pending'`. Once both rows process successfully, we `conn.commit()`.
*   **Rollback Condition:** If the resident specifies `end_times` violating checks, or the resident possesses overdue payments activating a hard-blocked MySQL Database Trigger `trg_check_overdue_payments`, the Python endpoint explicitly encounters the returned MySQL `SIGNAL SQLSTATE '45000'` crash, firing `conn.rollback()` ensuring half-completed bookings are eradicated.

---

## 4. Raw SQL & Connection Pooling Strategy

*   **Raw Parameterized Queries:** Standard Object Relational Mapping implementations (like SQLAlchemy) were completely ignored. Every query is written manually to maintain tight control. String bindings are supplied strictly via `(%s, %s, %s)` parameterization tuples inside standard Python `cursor.execute()` calls to entirely negate all possibilities of SQL Injection vulnerabilities without manually sanitizing arrays.
*   **Connection Pooling:** Reconnecting dynamically to MySQL on a per-request basis adds tremendous latency. Thus, globally, the application mounts `mysql.connector.pooling.MySQLConnectionPool` immediately upon booting via caching. Every HTTP route instantly grabs a pre-authorized thread-safe connection pipe array via `get_db_connection()` and reliably closes/releases the port when finalizing responses.

---

## 5. Key Design Decisions & Tradeoffs

1.  **Flask over Django/FastAPI:** We specifically chose Flask due to its extreme modularity over thick opinionated frameworks like Django, explicitly helping us conform to the stringent "No ORM" requirement natively by letting us plug Python's fastest low-level C-extension MySQL connector without framework-friction. 
2.  **Stateless Storage over Sessions:** We rejected Server-side Sessions (Memcached/Redis) tracking and favored standard `Authorization: Bearer <Token>` stateless setups. This inherently forces a lower memory footprint on the API Application processes and enables us to instantly scale our container horizontally.
3.  **Database-Defined Logic:** By offloading complex checks like 'overdue payment denial constraints' into DB Triggers (`trg_check_overdue_payments`), we maintained a unified Single Source of Truth, sacrificing mild code readability in Python for absolute unbreakable logical compliance on the Application level despite race conditions.
