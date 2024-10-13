from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# 數據庫連接
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='pet_database',
        user='root',  # 替換為你的 MySQL 用戶名
        password='Password0206!'  # 替換為你的 MySQL 密碼
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    position = request.form['position']
    major = request.form['major']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, position, major) VALUES (%s, %s, %s, %s)',
                   (name, age, position, major))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
