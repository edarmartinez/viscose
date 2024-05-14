-- Creating the Students table
CREATE TABLE IF NOT EXISTS Students (
    sid varchar(255) PRIMARY KEY,
    sname varchar(255) NOT NULL,
    age integer
);

-- Creating the Enrolled table
CREATE TABLE IF NOT EXISTS Enrolled (
    sid varchar(255),
    cid integer,
    grade varchar(255),
    FOREIGN KEY (sid) REFERENCES Students(sid)
);

-- Creating the Courses table
CREATE TABLE IF NOT EXISTS Courses (
    cid integer PRIMARY KEY,
    cname varchar(255),
    credits integer
);

-- Inserting records into Students
INSERT INTO Students (sid, sname, age) VALUES
('S001', 'Alice Smith', 20),
('S002', 'Bob Johnson', 21),
('S003', 'Carol Davis', 22),
('S004', 'David Martinez', 23),
('S005', 'Eve Brown', 24);

-- Inserting records into Courses
INSERT INTO Courses (cid, cname, credits) VALUES
(101, 'Introduction to Computer Science', 4),
(102, 'Computer Networks', 3),
(103, 'Computer Science Theory', 3),
(104, 'Database Systems', 4),
(105, 'Fundamentals of Programming', 3);

-- Inserting records into Enrolled
INSERT INTO Enrolled (sid, cid, grade) VALUES
('S001', 101, 'A'),
('S001', 102, 'B'),
('S002', 101, 'B'),
('S002', 103, 'A'),
('S003', 104, 'B'),
('S003', 105, 'A'),
('S004', 102, 'C'),
('S004', 103, 'B'),
('S005', 101, 'A'),
('S005', 104, 'A');

