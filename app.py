from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        student_name = request.form.get('student')
        rating = request.form.get("rating")
        topic = request.form.get('topic')
        comments = request.form.get('comments')
        if student_name == "" or topic == "" or comments == "":
            return render_template('home.html', message="Please input all required fields!")
        return redirect(url_for('success'))  # Change this line


@app.route("/submit", methods=["GET"])
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run()
