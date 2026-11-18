CREATE TABLE department (
    dept_id   NUMBER(4) PRIMARY KEY,
    dept_name VARCHAR2(40) UNIQUE,
    hod_name  VARCHAR2(40)
);
select * from department;