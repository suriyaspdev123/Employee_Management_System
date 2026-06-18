from flask import Flask, jsonify
import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database Connection Function
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


# Get Employee by ID
@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM employee WHERE employee_id=%s"
    cursor.execute(query, (id,))
    employee = cursor.fetchone()
    conn.close()
    if employee:
        return jsonify(employee)
    return jsonify({
        "message": "Employee not found"
    }), 404


# POST Employee
@app.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO employee
    (
        employee_name,
        email_id,
        department,
        salary,
        joining_date
    )
    VALUES
    (%s,%s,%s,%s,%s)
    """
    values = (
        data['employee_name'],
        data['email_id'],
        data['department'],
        data['salary'],
        data['joining_date']
    )
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Employee added successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)