from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pymysql
from pymysql.cursors import DictCursor
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,
    origins="http://localhost:5173"
)

app.config["SECRET_KEY"] = "sriram_jwt_secret_key_24"

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="#Sriraman24",
        database="hotel_db",
        cursorclass=DictCursor
    )

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated():
        token = request.cookies.get("token")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            decoded = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
            request.user_id = decoded["user_id"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f()

    return decorated

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username and not password:
        return jsonify({"error": "Please send username and password"}), 400

    if not username:
        return jsonify({"error": "Please send username"}), 400

    if not password:
        return jsonify({"error": "Please send password"}), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User does not exist in database"}), 401

        if user["is_locked"]:
            return jsonify({"error": "Too many failed attempts. Account locked."}), 403

        if user["password"] != password:
            new_attempts = user["failed_attempts"] + 1

            if new_attempts >= 6:
                cursor.execute(
                    "UPDATE users SET failed_attempts=%s, is_locked=TRUE WHERE id=%s",
                    (new_attempts, user["id"])
                )
                conn.commit()
                return jsonify({"error": "Too many failed attempts. Account locked."}), 403

            cursor.execute(
                "UPDATE users SET failed_attempts=%s WHERE id=%s",
                (new_attempts, user["id"])
            )
            conn.commit()

            attempts_left = 6 - new_attempts

            if attempts_left <= 3:
                return jsonify({
                    "error": "Invalid username or password",
                    "message": f"You have {attempts_left} attempts left"
                }), 401

            return jsonify({"error": "Invalid username or password"}), 401

        cursor.execute(
            "UPDATE users SET failed_attempts=0 WHERE id=%s",
            (user["id"],)
        )
        conn.commit()

        token = generate_token(user["id"])

        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            "token",
            token,
            httponly=True,
            secure=False,   
            samesite="Lax",
            max_age=3600
        )

        return response

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"message": "Logged out"})
    resp.set_cookie("token", "", expires=0)
    return resp

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

@app.route("/")
def home():
    return "Vanakkam da mapla!"

if __name__ == "__main__":
    app.run(debug=True)
