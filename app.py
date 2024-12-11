from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用於 flash 消息

# MongoDB 連接
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    db = client['sign_in_system']
    collection = db['employees']
    client.server_info()  # 測試連接是否成功
except Exception as e:
    print(f"無法連接到 MongoDB: {e}")
    exit(1)

# 首頁：顯示員工列表
@app.route('/')
def index():
    try:
        employees = list(collection.find())
        return render_template('index.html', employees=employees)
    except Exception as e:
        flash(f'獲取員工列表時發生錯誤: {e}', 'error')
        return render_template('index.html', employees=[])

# 搜索員工
@app.route('/search_employee', methods=['GET', 'POST'])
def search_employee():
    if request.method == 'POST':
        search_query = request.form.get('query', '').strip()
        if search_query:
            try:
                # 在 MongoDB 中搜索匹配名稱的員工
                employees = list(collection.find({'name': {'$regex': search_query, '$options': 'i'}}))
                if employees:
                    flash(f'找到 {len(employees)} 位符合條件的員工！', 'success')
                else:
                    flash('沒有找到符合條件的員工。', 'warning')
                return render_template('index.html', employees=employees)
            except Exception as e:
                flash(f'搜索員工時發生錯誤: {e}', 'error')
        else:
            flash('搜索條件不能為空！', 'warning')
    return redirect(url_for('index'))

# 添加員工
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        position = request.form.get('position', '').strip()
        company = request.form.get('company', '').strip()
        phone = request.form.get('phone', '').strip()

        if not name or not position or not company or not phone:
            flash('所有欄位均為必填！', 'warning')
            return render_template('add.html')

        try:
            collection.insert_one({
                'name': name,
                'position': position,
                'company': company,
                'phone': phone
            })
            flash('員工添加成功！', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'添加員工時發生錯誤: {e}', 'error')

    return render_template('add.html')

# 編輯員工
@app.route('/edit/<employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    try:
        employee = collection.find_one({'_id': ObjectId(employee_id)})
        if not employee:
            flash('未找到該員工。', 'warning')
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            position = request.form.get('position', '').strip()
            company = request.form.get('company', '').strip()
            phone = request.form.get('phone', '').strip()

            if not name or not position or not company or not phone:
                flash('所有欄位均為必填！', 'warning')
                return render_template('edit.html', employee=employee)

            collection.update_one({'_id': ObjectId(employee_id)}, {
                '$set': {
                    'name': name,
                    'position': position,
                    'company': company,
                    'phone': phone
                }
            })
            flash('員工資料更新成功！', 'success')
            return redirect(url_for('index'))

        return render_template('edit.html', employee=employee)

    except Exception as e:
        flash(f'編輯員工時發生錯誤: {e}', 'error')
        return redirect(url_for('index'))

# 刪除員工
@app.route('/delete/<employee_id>')
def delete_employee(employee_id):
    try:
        result = collection.delete_one({'_id': ObjectId(employee_id)})
        if result.deleted_count > 0:
            flash('員工刪除成功！', 'success')
        else:
            flash('未找到該員工。', 'warning')
    except Exception as e:
        flash(f'刪除員工時發生錯誤: {e}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
