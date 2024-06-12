import os
from datetime import date

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")

ENV = "prod"

if ENV == "dev":
    app.debug = True
    # Format for connecting to local database: "postgresql://username:password@localhost/database_name"
    app.config["SQLALCHEMY_DATABASE_URI"] = ""
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Review(db.Model):
    __tablename__ = "review"
    roll_no = db.Column(db.String(8), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Date, default=db.func.current_date())

    def __init__(self, roll_number, today_date, rating, topic, comments):
        self.roll_no = roll_number
        self.date = today_date
        self.rating = rating
        self.topic = topic
        self.comments = comments


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        roll_number = request.form.get("roll_number")
        roll_number = roll_number.upper()
        rating = int(request.form.get("rating"))
        topic = request.form.get("topic")
        comments = request.form.get("comments")
        today_date = date.today().strftime("%Y-%m-%d")

        if roll_number == "" or topic == "" or comments == "":
            return render_template(
                "home.html", message="Please input all required fields!"
            )
        else:
            if (
                db.session.query(Review)
                .filter(Review.roll_no == roll_number, Review.date == today_date)
                .count()
                == 0
            ):
                review = Review(roll_number, today_date, rating, topic, comments)
                db.session.add(review)
                db.session.commit()
                return redirect(url_for("success"))
        return render_template(
            "home.html", message="You have already given your feedback!"
        )


@app.route("/submit", methods=["GET"])
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run()
