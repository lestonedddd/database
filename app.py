# app.py
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL 配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password0206!',
    'database': 'restaurant_db'
}

# 創建數據庫連接
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 創建資料表（首次運行時使用）
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            rating INT NOT NULL,
            price INT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# 首頁路由 - 顯示表單和現有數據
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM restaurants')
    restaurants = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', restaurants=restaurants)

# 添加餐廳
@app.route('/add', methods=['POST'])
def add_restaurant():
    name = request.form['name']
    rating = request.form['rating']
    price = request.form['price']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO restaurants (name, rating, price) VALUES (%s, %s, %s)',
                  (name, rating, price))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# 更新餐廳
@app.route('/update/<int:id>', methods=['POST'])
def update_restaurant(id):
    name = request.form['name']
    rating = request.form['rating']
    price = request.form['price']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE restaurants SET name=%s, rating=%s, price=%s WHERE id=%s',
                  (name, rating, price, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# 刪除餐廳
@app.route('/delete/<int:id>')
def delete_restaurant(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM restaurants WHERE id=%s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# 顯示統計數據
@app.route('/join')
def join():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT name, rating, price FROM restaurants')
    restaurants = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('join.html', restaurants=restaurants)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)