from flask import Flask, jsonify, request, render_template, send_from_directory
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

DATABASE = "todo.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/tasks")
def get_tasks():
    conn = get_db()

    tasks = conn.execute("""
        SELECT id, title, completed
        FROM tasks
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "id": task["id"],
            "title": task["title"],
            "completed": bool(task["completed"])
        }
        for task in tasks
    ])


@app.post("/api/tasks")
def create_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    title = data["title"].strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = get_db()

    cursor = conn.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": task_id,
        "title": title,
        "completed": False
    }), 201


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json()

    if not data or "completed" not in data:
        return jsonify({"error": "completed is required"}), 400

    completed = 1 if data["completed"] else 0

    conn = get_db()

    cursor = conn.execute(
        """
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
        """,
        (completed, task_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.close()

    return jsonify({"success": True})


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.close()

    return jsonify({"success": True})


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
