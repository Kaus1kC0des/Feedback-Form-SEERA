from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kausik:goddamndev@localhost/reviews"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ""


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Review(db.Model):
    __tablename__ = 'review'
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
        roll_number = request.form.get('roll_number')
        rating = request.form.get("rating")
        topic = request.form.get('topic')
        comments = request.form.get('comments')
        today_date = date.today().strftime("%Y-%m-%d")

        if roll_number == "" or topic == "" or comments == "":
            return render_template('home.html', message="Please input all required fields!")
        else:
            if db.session.query(Review).filter(Review.roll_no == roll_number, Review.date == today_date).count() == 0:
                review = Review(roll_number, today_date, rating, topic, comments)
                db.session.add(review)
                db.session.commit()
                return redirect(url_for('success'))
        return redirect(url_for('success'))  # Change this line


@app.route("/submit", methods=["GET"])
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run()
