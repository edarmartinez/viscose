import mysql.connector
from mysql.connector import Error

# Creates database connection.
def create_connection(db_host, db_user, db_password, db_name):
    conn = None
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='7Passwordt53',
            database='project'
        )
    except Error as e:
        print(e)
    return conn

# Creates Students, Enrolled, and Courses tables in the database.
def create_tables(conn):
    if conn is not None:
        sql_create_students_table = """CREATE TABLE IF NOT EXISTS Students (
                                       sid varchar(255) PRIMARY KEY,
                                       sname varchar(255) NOT NULL,
                                       age integer);"""
        sql_create_enrolled_table = """CREATE TABLE IF NOT EXISTS Enrolled (
                                       sid varchar(255),
                                       cid integer,
                                       grade varchar(255),
                                       FOREIGN KEY (sid) REFERENCES Students(sid));"""
        sql_create_courses_table = """CREATE TABLE IF NOT EXISTS Courses (
                                       cid integer PRIMARY KEY,
                                       cname varchar(255),
                                       credits integer);"""
        try:
            c = conn.cursor()
            c.execute(sql_create_students_table)
            c.execute(sql_create_enrolled_table)
            c.execute(sql_create_courses_table)
        except Error as e:
            print(e)
    else:
        print("Can not create the database connection.")

# Creates a new student record.
def create_student(conn, sid, sname, age):
    sql = "INSERT INTO Students(sid, sname, age) VALUES(%s, %s, %s)"
    values = (sid, sname, age)
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    except Error as e:
        print(e)


# Creates a new enrollment record.
def create_enrollment(conn, sid, cid, grade):
    sql = "INSERT INTO Enrolled(sid, cid, grade) VALUES(%s, %s, %s)"
    values = (sid, cid, grade)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()

# Creates a new Course record.
def create_course(conn, cid, cname, credits):
    sql = "INSERT INTO Courses(cid, cname, credits) VALUES(%s, %s, %s)"
    values = (cid, cname, credits)
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    except Error as e:
        print(e)


# Shows a list of functions the user can execute.
def show_help_prompt():
    print("Help:")
    print("L: List all available courses",
          "\nE: Enroll yourself in a course",
          "\nW: Withdraw yourself from a course",
          "\nS: Search for a course by name",
          "\nM: List your current enrollments",
          "\nH: List executable functions",
          "\nX: Exit application")

def check_if_sid_exists(conn, sid):
    cur = conn.cursor()
    cur.execute("SELECT sid FROM Students WHERE sid = %s", (sid,))
    return cur.fetchone() is not None

# Helper function to get the student name.
def get_student_name(conn, sid):
    cur = conn.cursor()
    cur.execute("SELECT sname FROM Students WHERE sid = %s", (sid,))
    return cur.fetchone()[0]

# Function to list all available courses.
def select_all_courses(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Courses")
        courses = cur.fetchall()
        return courses
    except Error as e:
        print(e)
        return []



# Function to enroll a student in a course.
def enroll_in_course(conn, sid):
    cid = int(input("Enter course ID to enroll: "))
    cur = conn.cursor()
    cur.execute("SELECT * FROM Enrolled WHERE sid = %s AND cid = %s", (sid, cid))
    if cur.fetchone():
        print("You are already enrolled in this course.")
    else:
        create_enrollment(conn, sid, cid, "Not Graded")

# Function to withdraw a student from a course.
def withdraw_from_course(conn, sid):
    cid = int(input("Enter course ID to withdraw from: "))
    cur = conn.cursor()
    cur.execute("DELETE FROM Enrolled WHERE sid = %s AND cid = %s", (sid, cid))
    conn.commit()
    print("Withdrawn from course", cid)

# Function to search for a course by name.
def search_for_course(conn):
    search_term = input("Enter a substring to search for in course names: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses WHERE cname LIKE %s", ('%'+search_term+'%',))
    courses = cur.fetchall()
    for course in courses:
        print(course)

# Function to list all classes a student is enrolled in.
def view_my_classes(conn, sid):
    cur = conn.cursor()
    cur.execute    ("SELECT Courses.cid, Courses.cname FROM Courses JOIN Enrolled ON Courses.cid = Enrolled.cid WHERE Enrolled.sid = %s", (sid,))
    courses = cur.fetchall()
    for course in courses:
        print(course)

# Function to create a new student.
def create_new_student(conn):
    sid = input("Enter your student ID: ")
    sname = input("Enter your name: ")
    age = int(input("Enter your age: "))
    create_student(conn, sid, sname, age)
    return sid

# Modified start_cmd_interface function
def start_cmd_interface(conn):
    print("Welcome to MSU Course Registration System!")
    sid_input = input("Enter your student id (or enter -1 to sign up): ")

    if sid_input == '-1':
        sid = create_new_student(conn)
    elif not check_if_sid_exists(conn, sid_input):
        print("Student id does not exist in the database. Please sign up.")
        return
    else:
        sid = sid_input

    print("Welcome back", get_student_name(conn, sid), "!")

    while True:
        userInput = input("Enter a command (L, E, W, S, M, H, X): ")
        if userInput == 'L':
            courses = select_all_courses(conn)
            if courses:
                for course in courses:
                    print(course)
            else:
                print("No courses available.")
        elif userInput == 'E':
            enroll_in_course(conn, sid)
        elif userInput == 'W':
            withdraw_from_course(conn, sid)
        elif userInput == 'S':
            search_for_course(conn)
        elif userInput == 'M':
            view_my_classes(conn, sid)
        elif userInput == 'H':
            show_help_prompt()
        elif userInput == 'X':
            print("Thank you for using MSU Course Registration System!")
            break
        else:
            print("Not a valid command (enter H for help).")

def select_all_students(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students")
        students = cur.fetchall()
        return students
    except Error as e:
        print(e)
        return []



# Main method.
def main():
    db_host = 'your_host'
    db_user = 'your_username'
    db_password = 'your_password'
    db_name = 'your_dbname'
    conn = create_connection(db_host, db_user, db_password, db_name)

    if conn is not None:
        create_tables(conn)
        start_cmd_interface(conn)
    else:
        print("Failed to establish a database connection.")

if __name__ == "__main__":
    main()



