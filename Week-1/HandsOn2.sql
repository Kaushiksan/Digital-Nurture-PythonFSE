-- =====================================================
-- HANDS-ON 2
-- SQL Queries (DML, Joins & Aggregations)
-- =====================================================

USE college_db;

-- =====================================================
-- TASK 1 : INSERT DATA
-- =====================================================

-- Departments

INSERT INTO departments
(dept_name, head_of_dept, budget)
VALUES
('Computer Science','Dr. Ramesh Kumar',850000.00),
('Electronics','Dr. Priya Nair',620000.00),
('Mechanical','Dr. Suresh Iyer',540000.00),
('Civil','Dr. Ananya Sharma',430000.00);

-- Students

INSERT INTO students
(first_name,last_name,email,date_of_birth,department_id,enrollment_year)
VALUES
('Arjun','Mehta','arjun.mehta@college.edu','2003-04-12',1,2022),
('Priya','Suresh','priya.suresh@college.edu','2003-07-25',1,2022),
('Rohan','Verma','rohan.verma@college.edu','2002-11-08',2,2021),
('Sneha','Patel','sneha.patel@college.edu','2004-01-30',3,2023),
('Vikram','Das','vikram.das@college.edu','2003-09-14',1,2022),
('Kavya','Menon','kavya.menon@college.edu','2002-05-17',2,2021),
('Aditya','Singh','aditya.singh@college.edu','2004-03-22',4,2023),
('Deepika','Rao','deepika.rao@college.edu','2003-08-09',1,2022),
('Rahul','Sharma','rahul.sharma@college.edu','2003-02-10',1,2022),
('Nisha','Kapoor','nisha.kapoor@college.edu','2004-08-20',2,2023);

-- Courses

INSERT INTO courses
(course_name,course_code,credits,department_id)
VALUES
('Data Structures and Algorithms','CS101',4,1),
('Database Management Systems','CS102',3,1),
('Object Oriented Programming','CS103',4,1),
('Circuit Theory','EC101',3,2),
('Thermodynamics','ME101',3,3);

-- Professors

INSERT INTO professors
(prof_name,email,department_id,salary)
VALUES
('Dr. Anand Krishnan','anand.k@college.edu',1,95000),
('Dr. Meena Pillai','meena.p@college.edu',1,88000),
('Dr. Sunil Rajan','sunil.r@college.edu',2,82000),
('Dr. Latha Gopal','latha.g@college.edu',3,79000),
('Dr. Kartik Bose','kartik.b@college.edu',4,76000);

-- Enrollments

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(1,1,'2022-07-01','A'),
(1,2,'2022-07-01','B'),
(2,1,'2022-07-01','B'),
(2,3,'2022-07-01','A'),
(3,4,'2021-07-01','A'),
(4,5,'2023-07-01',NULL),
(5,1,'2022-07-01','C'),
(5,2,'2022-07-01','A'),
(6,4,'2021-07-01','B'),
(7,5,'2023-07-01',NULL),
(8,1,'2022-07-01','A'),
(8,3,'2022-07-01','B');

-- =====================================================
-- TASK 2 : UPDATE & DELETE
-- =====================================================

UPDATE enrollments
SET grade='B'
WHERE student_id=5
AND course_id=1;

SELECT *
FROM enrollments
WHERE grade IS NULL;

DELETE FROM enrollments
WHERE grade IS NULL;

SELECT COUNT(*) AS Student_Count
FROM students;

SELECT COUNT(*) AS Enrollment_Count
FROM enrollments;

-- =====================================================
-- TASK 3 : SINGLE TABLE QUERIES
-- =====================================================

-- Students enrolled in 2022

SELECT
student_id,
first_name,
last_name,
email
FROM students
WHERE enrollment_year=2022
ORDER BY last_name;

-- Courses having credits greater than 3

SELECT
course_name,
credits
FROM courses
WHERE credits>3
ORDER BY credits DESC;

-- Professors earning between 80K and 95K

SELECT
prof_name,
salary
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

-- Students with email ending in @college.edu

SELECT
student_id,
first_name,
email
FROM students
WHERE email LIKE '%@college.edu';

-- Count students by enrollment year

SELECT
enrollment_year,
COUNT(*) AS Total_Students
FROM students
GROUP BY enrollment_year;

-- =====================================================
-- TASK 4 : JOINS
-- =====================================================

-- 1. Display each student with their department

SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS Student_Name,
    d.dept_name
FROM students s
INNER JOIN departments d
ON s.department_id = d.department_id
ORDER BY Student_Name;

---------------------------------------------------------

-- 2. Display students with enrolled courses and grades

SELECT
    CONCAT(s.first_name,' ',s.last_name) AS Student_Name,
    c.course_name,
    e.grade
FROM enrollments e
INNER JOIN students s
ON e.student_id = s.student_id
INNER JOIN courses c
ON e.course_id = c.course_id
ORDER BY Student_Name;

---------------------------------------------------------

-- 3. Students not enrolled in any course

SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS Student_Name
FROM students s
LEFT JOIN enrollments e
ON s.student_id = e.student_id
WHERE e.student_id IS NULL;

---------------------------------------------------------

-- 4. Courses with number of students enrolled

SELECT
    c.course_id,
    c.course_name,
    COUNT(e.student_id) AS Total_Students
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id,c.course_name
ORDER BY Total_Students DESC;

---------------------------------------------------------

-- 5. Display departments with professors

SELECT
    d.dept_name,
    p.prof_name,
    p.salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id
ORDER BY d.dept_name;

-- =====================================================
-- TASK 5 : AGGREGATE FUNCTIONS
-- =====================================================

-- 1. Total enrollments per course

SELECT
    c.course_name,
    COUNT(e.student_id) AS Enrollment_Count
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id,c.course_name
ORDER BY Enrollment_Count DESC;

---------------------------------------------------------

-- 2. Average professor salary per department

SELECT
    d.dept_name,
    ROUND(AVG(p.salary),2) AS Average_Salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id
GROUP BY d.department_id,d.dept_name;

---------------------------------------------------------

-- 3. Departments with budget above 600000

SELECT
    dept_name,
    budget
FROM departments
WHERE budget > 600000;

---------------------------------------------------------

-- 4. Grade distribution for CS101

SELECT
    e.grade,
    COUNT(*) AS Total_Students
FROM enrollments e
INNER JOIN courses c
ON e.course_id = c.course_id
WHERE c.course_code='CS101'
GROUP BY e.grade
ORDER BY e.grade;

---------------------------------------------------------

-- 5. Departments having more than two students

SELECT
    d.dept_name,
    COUNT(s.student_id) AS Total_Students
FROM departments d
INNER JOIN students s
ON d.department_id = s.department_id
GROUP BY d.department_id,d.dept_name
HAVING COUNT(s.student_id) > 2;

-- =====================================================
-- TASK 6 : VERIFICATION QUERIES
-- =====================================================

-- Verify Departments

SELECT *
FROM departments;

---------------------------------------------------------

-- Verify Students

SELECT *
FROM students;

---------------------------------------------------------

-- Verify Courses

SELECT *
FROM courses;

---------------------------------------------------------

-- Verify Enrollments

SELECT *
FROM enrollments;

---------------------------------------------------------

-- Verify Professors

SELECT *
FROM professors;

-- =====================================================
-- TASK 7 : SUMMARY REPORTS
-- =====================================================

-- Total Departments

SELECT
COUNT(*) AS Total_Departments
FROM departments;

---------------------------------------------------------

-- Total Students

SELECT
COUNT(*) AS Total_Students
FROM students;

---------------------------------------------------------

-- Total Courses

SELECT
COUNT(*) AS Total_Courses
FROM courses;

---------------------------------------------------------

-- Total Professors

SELECT
COUNT(*) AS Total_Professors
FROM professors;

---------------------------------------------------------

-- Total Enrollments

SELECT
COUNT(*) AS Total_Enrollments
FROM enrollments;

---------------------------------------------------------

-- Highest Professor Salary

SELECT
MAX(salary) AS Highest_Salary
FROM professors;

---------------------------------------------------------

-- Lowest Professor Salary

SELECT
MIN(salary) AS Lowest_Salary
FROM professors;

---------------------------------------------------------

-- Average Professor Salary

SELECT
ROUND(AVG(salary),2) AS Average_Salary
FROM professors;

---------------------------------------------------------

-- Total Department Budget

SELECT
SUM(budget) AS Total_Budget
FROM departments;

-- =====================================================
-- COMMENTS
-- =====================================================

/*
Hands-On 2
-----------
Module      : Database Integration
Topic       : SQL Queries (DML, Joins & Aggregations)

Concepts Covered
----------------
1. INSERT
2. UPDATE
3. DELETE
4. SELECT
5. WHERE
6. LIKE
7. ORDER BY
8. INNER JOIN
9. LEFT JOIN
10. Aggregate Functions
11. GROUP BY
12. HAVING
13. COUNT()
14. AVG()
15. SUM()
16. MIN()
17. MAX()
18. ROUND()

Expected Outcome
----------------
✔ Sample data inserted successfully.
✔ Student grade updated.
✔ NULL grade enrollments removed.
✔ Join queries executed successfully.
✔ Aggregate reports generated.
✔ Verification queries executed successfully.

Status : COMPLETED
*/

-- =====================================================
-- END OF HANDS-ON 2
-- =====================================================
