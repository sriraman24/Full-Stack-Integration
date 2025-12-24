from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from pymysql.cursors import DictCursor
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# ================= CORS (CORRECT FOR COOKIES) =================
CORS(
    app,
    supports_credentials=True,
    origins="http://localhost:5173"
)

app.config["SECRET_KEY"] = "sriram_jwt_secret_key_24"

# ================= DATABASE =================
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="#Sriraman24",
        database="hotel_db",
        cursorclass=DictCursor
    )

# ================= JWT =================
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["id"])

    resp = jsonify({"message": "Login successful"})
    resp.set_cookie(
        "token",
        token,
        httponly=True,
        samesite="Lax",
        secure=False
    )
    return resp

# ================= LOGOUT =================
@app.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"message": "Logged out"})
    resp.set_cookie("token", "", expires=0)
    return resp

# ================= GET ORDERS =================
@app.route("/orders", methods=["GET"])
@token_required
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(orders)

# ================= ADD ORDER =================
@app.route("/add-order", methods=["POST"])
@token_required
def add_order():
    data = request.get_json()
    order_id = data.get("order_id")
    customer = data.get("customer_name")
    item = data.get("item")

    if not order_id or not customer or not item:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (order_id, customer_name, item) VALUES (%s,%s,%s)",
        (order_id, customer, item)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order added"})

# ================= UPDATE ORDER =================
@app.route("/update-order", methods=["PUT"])
@token_required
def update_order():
    data = request.get_json()
    order_id = data.get("order_id")
    item = data.get("item")

    if not order_id or not item:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET item=%s WHERE order_id=%s",
        (item, order_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order updated"})

# ================= DELETE ORDER =================
@app.route("/delete-order", methods=["DELETE"])
@token_required
def delete_order():
    data = request.get_json()
    order_id = data.get("order_id")

    if not order_id:
        return jsonify({"error": "Missing order_id"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order deleted"})

# ================= HOME =================
@app.route("/")
def home():
    return "Backend running 🚀"

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
