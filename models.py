from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String,
        unique=True,
        nullable=False
    )

    _password_hash = db.Column(db.String, nullable=False)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required.")

        return username

    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String,
        nullable=False
    )

    description = db.Column(db.String)

    completed = db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    user = db.relationship(
        "User",
        back_populates="tasks"
    )

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Task title is required.")

        return title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "user_id": self.user_id
        }




