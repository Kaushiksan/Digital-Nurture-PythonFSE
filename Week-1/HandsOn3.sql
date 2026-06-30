-- =====================================================
-- HANDS-ON 3
-- Advanced SQL – Subqueries, Views & Transactions
-- =====================================================

USE college_db;

-- =====================================================
-- TASK 1 : SUBQUERIES
-- =====================================================

-- 1. Students enrolled in more courses than the average

SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS Student_Name,
    COUNT(e.course_id) AS Total_Courses
FROM students s
JOIN enrollments e
ON s.student_id=e.student_id
GROUP BY s.student_id,s.first_name,s.last_name
HAVING COUNT(e.course_id) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_table
);

---------------------------------------------------------

-- 2. Courses where every student received Grade A

SELECT
    c.course_id,
    c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id=c.course_id
    AND e.grade<>'A'
);

---------------------------------------------------------

-- 3. Highest paid professor in every department

SELECT
    p.prof_name,
    d.dept_name,
    p.salary
FROM professors p
JOIN departments d
ON p.department_id=d.department_id
WHERE salary=
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id=p.department_id
);

---------------------------------------------------------

-- 4. Departments whose average salary exceeds 85000

SELECT
    dept_name,
    Average_Salary
FROM
(
    SELECT
        d.dept_name,
        AVG(p.salary) AS Average_Salary
    FROM departments d
    JOIN professors p
    ON d.department_id=p.department_id
    GROUP BY d.dept_name
) AS salary_table
WHERE Average_Salary>85000;

-- =====================================================
-- TASK 2 : VIEWS
-- =====================================================

-- Drop views if they already exist

DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

---------------------------------------------------------
-- View 1 : Student Enrollment Summary
---------------------------------------------------------

CREATE VIEW vw_student_enrollment_summary AS

SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS Student_Name,
    d.dept_name,
    COUNT(e.course_id) AS Total_Courses,

    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS GPA

FROM students s

JOIN departments d
ON s.department_id=d.department_id

LEFT JOIN enrollments e
ON s.student_id=e.student_id

GROUP BY
s.student_id,
Student_Name,
d.dept_name;

---------------------------------------------------------
-- View 2 : Course Statistics
---------------------------------------------------------

CREATE VIEW vw_course_stats AS

SELECT

    c.course_name,
    c.course_code,

    COUNT(e.student_id) AS Total_Enrollments,

    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS Average_GPA

FROM courses c

LEFT JOIN enrollments e
ON c.course_id=e.course_id

GROUP BY
c.course_id,
c.course_name,
c.course_code;

---------------------------------------------------------
-- Query View 1
---------------------------------------------------------

SELECT *
FROM vw_student_enrollment_summary
WHERE GPA>3.0;

---------------------------------------------------------
-- Query View 2
---------------------------------------------------------

SELECT *
FROM vw_course_stats;

---------------------------------------------------------
-- Attempt to Update View
---------------------------------------------------------

UPDATE vw_student_enrollment_summary
SET Student_Name='Demo'
WHERE student_id=1;

-- NOTE:
-- Multi-table views are generally NOT updatable because
-- the database cannot determine which underlying table(s)
-- should be modified.

---------------------------------------------------------
-- Recreate View with CHECK OPTION
---------------------------------------------------------

DROP VIEW vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS

SELECT
student_id,
first_name,
last_name,
department_id

FROM students

WHERE department_id=1

WITH CHECK OPTION;

-- =====================================================
-- TASK 3 : STORED PROCEDURES & TRANSACTIONS
-- =====================================================

-- -----------------------------------------------------
-- Create Transfer Log Table
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS department_transfer_log
(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Stored Procedure : Enroll Student
-- -----------------------------------------------------

DELIMITER $$

CREATE PROCEDURE sp_enroll_student
(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN

    IF EXISTS
    (
        SELECT *
        FROM enrollments
        WHERE student_id=p_student_id
        AND course_id=p_course_id
    )
    THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Student already enrolled in this course';

    ELSE

        INSERT INTO enrollments
        (
            student_id,
            course_id,
            enrollment_date,
            grade
        )

        VALUES
        (
            p_student_id,
            p_course_id,
            p_enrollment_date,
            NULL
        );

    END IF;

END$$

DELIMITER ;

-- -----------------------------------------------------
-- Test Procedure
-- -----------------------------------------------------

CALL sp_enroll_student(3,2,'2024-06-01');

--------------------------------------------------------

-- Stored Procedure : Transfer Student

DELIMITER $$

CREATE PROCEDURE sp_transfer_student
(
    IN p_student INT,
    IN p_new_department INT
)

BEGIN

    DECLARE old_department INT;

    START TRANSACTION;

    SELECT department_id
    INTO old_department
    FROM students
    WHERE student_id=p_student;

    UPDATE students

    SET department_id=p_new_department

    WHERE student_id=p_student;

    INSERT INTO department_transfer_log
    (
        student_id,
        old_department,
        new_department
    )

    VALUES
    (
        p_student,
        old_department,
        p_new_department
    );

    COMMIT;

END$$

DELIMITER ;

--------------------------------------------------------

-- Test Procedure

CALL sp_transfer_student(2,3);

-- =====================================================
-- TRANSACTION DEMONSTRATION
-- =====================================================

START TRANSACTION;

UPDATE professors

SET salary=salary+5000

WHERE professor_id=1;

UPDATE professors

SET salary=salary+3000

WHERE professor_id=2;

COMMIT;

--------------------------------------------------------

-- ROLLBACK Example

START TRANSACTION;

UPDATE professors

SET salary=salary+2000

WHERE professor_id=3;

ROLLBACK;

--------------------------------------------------------

-- SAVEPOINT Example

START TRANSACTION;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)

VALUES
(6,2,CURDATE(),'A');

SAVEPOINT first_insert;

-- This may fail if duplicate exists

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)

VALUES
(6,2,CURDATE(),'A');

ROLLBACK TO first_insert;

COMMIT;

-- =====================================================
-- VERIFICATION
-- =====================================================

SELECT *
FROM department_transfer_log;

--------------------------------------------------------

SELECT *
FROM vw_student_enrollment_summary;

--------------------------------------------------------

SELECT *
FROM vw_course_stats;

--------------------------------------------------------

SHOW PROCEDURE STATUS
WHERE Db='college_db';

-- =====================================================
-- COMMENTS
-- =====================================================

/*
Hands-On 3
-----------

Topics Covered

1. Non-correlated Subqueries
2. Correlated Subqueries
3. Derived Tables
4. Views
5. Aggregate Views
6. Stored Procedures
7. Transactions
8. COMMIT
9. ROLLBACK
10. SAVEPOINT
11. SIGNAL
12. WITH CHECK OPTION

Expected Outcome

✔ Subqueries executed successfully.
✔ Views created successfully.
✔ GPA calculated using CASE expression.
✔ Stored procedures created.
✔ Transactions tested.
✔ SAVEPOINT demonstrated.
✔ Transfer log maintained.

Status : COMPLETED
*/

-- =====================================================
-- END OF HANDS-ON 3
-- =====================================================
