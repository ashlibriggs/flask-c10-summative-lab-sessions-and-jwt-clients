from flask import request, session, jsonify
from config import app, db
from models import User, Task


@app.route("/")
def index():
    return "<h1>Productivity App API</h1>"



@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    try:
        user = User(
            username=data["username"]
        )

        user.password_hash = data["password"]

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return jsonify(user.to_dict()), 201

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 422

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter(
        User.username == data["username"]
    ).first()

    if user and user.authenticate(data["password"]):
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/check_session")
def check_session():
    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
        return jsonify(user.to_dict()), 200

    return jsonify({"error": "Unauthorized"}), 401
    

@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)

    return "", 204


@app.route("/tasks")
def get_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = Task.query.filter(
        Task.user_id == user_id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    tasks = pagination.items

    return jsonify({
        "tasks": [task.to_dict() for task in tasks],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    task = Task(
        title=data["title"],
        description=data.get("description"),
        completed=data.get("completed", False),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@app.route("/tasks/<int:id>")
def get_task_by_id(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    task = Task.query.filter(
        Task.id == id,
        Task.user_id == user_id
    ).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict()), 200


@app.route("/tasks/<int:id>", methods=["PATCH"])
def update_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    task = Task.query.filter(
        Task.id == id,
        Task.user_id == user_id
    ).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()

    return jsonify(task.to_dict()), 200


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    task = Task.query.filter(
        Task.id == id,
        Task.user_id == user_id
    ).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return "", 204

if __name__ == "__main__":
    app.run(port=5555, debug=True)

