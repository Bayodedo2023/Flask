from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random string


# Database connection function
def get_db_connection():
    conn = sqlite3.connect('user_accounts.db')
    conn.row_factory = sqlite3.Row
    return conn


# Calculate grade route
@app.route('/', methods=['GET', 'POST'])
def calculate_grade():
    if request.method == 'POST':
        entry_grades = request.form['grades']
        entry_weights = request.form['weights']

        try:
            grades = [float(grade) for grade in entry_grades.split(",")]
            weights = [float(weight) for weight in entry_weights.split(",")]
        except ValueError:
            flash("Please enter valid grades and weights separated by commas.", "error")
            return redirect(url_for('calculate_grade'))

        if len(grades) != len(weights):
            flash("Number of grades and weights must match.", "error")
            return redirect(url_for('calculate_grade'))

        final_grade = sum(grade * weight for grade, weight in zip(grades, weights))
        flash(f"Your final grade is: {final_grade:.2f}", "success")

    return render_template('calculate_grade.html')


if __name__ == '__main__':
    app.run(debug=True)
