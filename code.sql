CREATE TABLE departments (id SERIAL PRIMARY KEY, name VARCHAR (50)) ;
CREATE TABLE employees (
  id SERIAL PRIMARY KEY, name VARCHAR(100),
  email VARCHAR (100), phone VARCHAR (20),
  department_id INT REFERENCES departments (id)
);
