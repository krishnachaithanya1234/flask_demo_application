from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def index():
    tasks = Task.query.all()
    logger.info("Homepage loaded.")
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    try:
        description = request.form.get("description")
        if not description:
            logger.warning("Empty task submitted.")
            return "Task cannot be empty", 400

        new_task = Task(description=description)
        db.session.add(new_task)
        db.session.commit()
        logger.info(f"Task added: {description}")
        return render_template("index.html", tasks=Task.query.all())

    except Exception as e:
        logger.error(f"Error adding task: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
