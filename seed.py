from config import app, db
from models import User, Task


with app.app_context():

    print("Deleting old data...")
    Task.query.delete()
    User.query.delete()

    print("Creating users...")

    user1 = User(username="ashli")
    user1.password_hash = "password123"

    user2 = User(username="bestie")
    user2.password_hash = "password123"

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Creating tasks...")

    task1 = Task(
        title="Finish Summative Lab",
        description="Complete all rubric requirements",
        completed=False,
        user_id=user1.id
    )

    task2 = Task(
        title="Study Python",
        description="Review loops and dictionaries",
        completed=False,
        user_id=user1.id
    )

    task3 = Task(
        title="Apply for apprenticeships",
        description="Submit at least three applications",
        completed=False,
        user_id=user2.id
    )

    db.session.add_all([task1, task2, task3])
    db.session.commit()

    print("Seeding complete!")
