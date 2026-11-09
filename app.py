import os

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def run_query(sql, params=None, fetch=False):
    conn = get_conn()
    try:
        with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None
    finally:
        conn.close()


def init_db():
    run_query(
        """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            min_stock INTEGER NOT NULL CHECK (min_stock >= 0),
            unit VARCHAR(20) NOT NULL DEFAULT 'pcs'
        )
        """
    )


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    try:
        run_query("SELECT 1")
        return jsonify(status="ok", database="up"), 200
    except Exception:
        return jsonify(status="error", database="down"), 503


@app.get("/items")
def list_items():
    rows = run_query("SELECT * FROM items ORDER BY id", fetch=True)
    return jsonify(rows), 200


@app.get("/items/low")
def low_stock():
    rows = run_query(
        "SELECT * FROM items WHERE quantity <= min_stock ORDER BY quantity, id",
        fetch=True,
    )
    return jsonify(rows), 200


@app.post("/items")
def add_item():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    name = name.strip() if isinstance(name, str) else ""
    unit = data.get("unit")
    unit = unit.strip() if isinstance(unit, str) and unit.strip() else "pcs"
    quantity = data.get("quantity")
    min_stock = data.get("min_stock")

    valid_numbers = all(
        isinstance(v, int) and not isinstance(v, bool) and v >= 0
        for v in (quantity, min_stock)
    )
    if not name or len(name) > 100 or not valid_numbers:
        return jsonify(error="name wajib diisi; quantity dan min_stock harus bilangan bulat >= 0"), 400

    rows = run_query(
        "INSERT INTO items (name, quantity, min_stock, unit) "
        "VALUES (%s, %s, %s, %s) RETURNING *",
        (name, quantity, min_stock, unit[:20]),
        fetch=True,
    )
    return jsonify(rows[0]), 201


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("APP_PORT", "5000")))