from flask import Flask, render_template, request, redirect, url_for, jsonify
import models

app = Flask(__name__)

# Database Connection
db_host = '127.0.0.1'
db_user = 'root'
db_password = '7Passwordt53'
db_name = 'project'
conn = models.create_connection(db_host, db_user, db_password, db_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def list_courses():
    courses = models.select_all_courses(conn)
    return render_template('courses.html', courses=courses)

@app.route('/students')
def list_students():
    students = models.select_all_students(conn)
    return render_template('students.html', students=students)

@app.route('/enroll', methods=['GET', 'POST'])
def enroll_course():
    if request.method == 'POST':
        # Add logic to handle enrollment form submission
        pass  # Replace 'pass' with your logic
    return render_template('enroll.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        sid = request.form['sid']
        sname = request.form['sname']
        age = request.form['age']
        models.create_student(conn, sid, sname, age)
        return redirect(url_for('list_students'))
    return render_template('add_student.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        cid = request.form['cid']
        cname = request.form['cname']
        credits = request.form['credits']
        models.create_course(conn, cid, cname, credits)
        return redirect(url_for('list_courses'))
    return render_template('add_course.html')
@app.route('/test_db')
def test_db():
    try:
        students = models.select_all_students(conn)
        if students:
            return jsonify(students)
        else:
            return "No students found or unable to fetch data from the database."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
