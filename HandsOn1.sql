-- ============================================
-- HANDS-ON 1
-- Schema Design & Core SQL
-- ============================================

-- ============================================
-- Task 1 : Create Database
-- ============================================

CREATE DATABASE college_db;

SHOW DATABASES;

USE college_db;

-- ============================================
-- Create Tables
-- ============================================

-- 1. Departments

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

-- 2. Students

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- 3. Courses

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- 4. Enrollments

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),

    CONSTRAINT fk_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    CONSTRAINT fk_course
        FOREIGN KEY (course_id)
        REFERENCES courses(course_id),

    CONSTRAINT uq_student_course
        UNIQUE(student_id, course_id)
);

-- 5. Professors

CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- ============================================
-- Verify Tables
-- ============================================

SHOW TABLES;

DESCRIBE departments;
DESCRIBE students;
DESCRIBE courses;
DESCRIBE enrollments;
DESCRIBE professors;

-- ============================================
-- Task 2 : Normalization
-- ============================================

/*
FIRST NORMAL FORM (1NF)

• Every table has a primary key.
• Every column stores only atomic (single) values.
• No repeating groups or multiple values are stored in one column.

Example:
Phone numbers should not be stored as
'9876543210,9123456789' in one field.
*/


/*
SECOND NORMAL FORM (2NF)

• All non-key attributes depend on the whole primary key.
• Student details belong only to Students.
• Course details belong only to Courses.
• Enrollment details depend only on the student-course enrollment.
*/


/*
THIRD NORMAL FORM (3NF)

• No transitive dependency exists.
• Department information is stored only in Departments.
• Students, Courses and Professors reference departments using department_id.
• This removes redundancy and prevents update anomalies.

Hence, the schema satisfies 3NF.
*/

-- ============================================
-- Task 3 : ALTER TABLE
-- ============================================

-- Add phone number

ALTER TABLE students
ADD phone_number VARCHAR(15);

-- Add maximum seats

ALTER TABLE courses
ADD max_seats INT DEFAULT 60;

-- Add CHECK constraint

ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Rename HOD column

ALTER TABLE departments
RENAME COLUMN hod_name TO head_of_dept;

-- Drop phone number

ALTER TABLE students
DROP COLUMN phone_number;

-- ============================================
-- Verification
-- ============================================

DESCRIBE departments;
DESCRIBE students;
DESCRIBE courses;
DESCRIBE enrollments;

SHOW COLUMNS FROM courses;

SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'college_db'
AND TABLE_NAME = 'courses';
