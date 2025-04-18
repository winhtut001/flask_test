from flask import Flask, render_template, request, redirect, url_for
from student_management import StudentManager
import sqlite3
import os

app = Flask(__name__)

# Use environment variable for database path
if os.environ.get('RENDER'):
    db_path = os.path.join(os.getcwd(), 'students.db')
else:
    db_path = '/Users/hanwinhtut/Documents/testing/flask_test/students.db'

student_manager = StudentManager(db_path)
student_manager.initialize_db()
student_manager.load_data()

# Initialize database and load data
student_manager.initialize_db()
student_manager.load_data()

# Add a debug print to check if students are loaded
print(f"Loaded {len(student_manager.students)} students from database")

@app.route("/")
def hello_world():
    return redirect(url_for('list_students'))

@app.route("/students", methods=["GET"])
def list_students():
    students = student_manager.students
    return render_template("students.html", students=students)

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("name")
        nickname = request.form.get("nickname")
        major = request.form.get("major")
        faculty = request.form.get("faculty")
        mat241_score = request.form.get("mat241_score", "N/A")
        
        student_manager.add_student(student_id, name, nickname, major, faculty, mat241_score)
        return redirect(url_for("list_students"))
    
    return render_template("add_student.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9000))
    app.run(host='0.0.0.0', port=port)
