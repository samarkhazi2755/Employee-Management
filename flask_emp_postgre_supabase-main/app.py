from flask import Flask, render_template, request, redirect, flash
from models import get_conn

app = Flask(__name__)
app.secret_key = "supabase-flask-secret"


def get_departments():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM departments")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows


@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, e.name, e.email, e.phone, d.name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
    """)
    employees = cur.fetchall()
    cur.close(); conn.close()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, email, phone, department_id) VALUES (%s, %s, %s, %s)",
            (request.form["name"], request.form["email"], request.form["phone"], request.form["department_id"])
        )
        conn.commit()
        cur.close(); conn.close()
        flash("Employee added successfully!", "success")
        return redirect("/")
    return render_template("add.html", departments=get_departments())


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute(
            "UPDATE employees SET name=%s, email=%s, phone=%s, department_id=%s WHERE id=%s",
            (request.form["name"], request.form["email"], request.form["phone"], request.form["department_id"], id)
        )
        conn.commit()
        cur.close(); conn.close()
        flash("Employee updated successfully!", "success")
        return redirect("/")
    cur.execute("SELECT id, name, email, phone, department_id FROM employees WHERE id=%s", (id,))
    employee = cur.fetchone()
    cur.close(); conn.close()
    return render_template("edit.html", employee=employee, departments=get_departments())


@app.route("/delete/<int:id>")
def delete_employee(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    cur.close(); conn.close()
    flash("Employee deleted.", "warning")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
