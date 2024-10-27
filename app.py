import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
from join import join_blueprint

app = Flask(__name__)

# 註冊藍圖
app.register_blueprint(join_blueprint)

# 設定密鑰以使用 flash 消息
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Password0206!',
            database='basketball'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    return render_template('template.html')

# 顯示所有球員
@app.route('/players')
def players():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Player')
    players = cursor.fetchall()
    conn.close()
    return render_template('players.html', players=players)

@app.route('/players/add', methods=('GET', 'POST'))
def add_player():
    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        if name and position:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Player (name, position) VALUES (%s, %s)', (name, position))
            conn.commit()
            conn.close()
            flash('Player added successfully!', 'success')
            return redirect(url_for('players'))
    return render_template('add_player.html')

# 刪除球員
@app.route('/players/delete/<int:id>', methods=('POST',))
def delete_player(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Player WHERE player_id = %s', (id,))
    conn.commit()
    conn.close()
    flash('Player deleted successfully!', 'success')
    return redirect(url_for('players'))

# 更新球員
@app.route('/players/update/<int:id>', methods=('GET', 'POST'))
def update_player(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Player WHERE player_id = %s', (id,))
    player = cursor.fetchone()

    if player is None:
        return "Player not found", 404

    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')

        if name and position:
            cursor.execute('UPDATE Player SET name = %s, position = %s WHERE player_id = %s', (name, position, id))
            conn.commit()
            flash('Player updated successfully!', 'success')
            return redirect(url_for('players'))

    conn.close()
    return render_template('update_player.html', player=player)

# 編輯統計
@app.route('/statistics/edit/<int:stat_id>', methods=('GET', 'POST'))
def edit_statistics(stat_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Stats WHERE stat_id = %s', (stat_id,))
    stat = cursor.fetchone()

    if stat is None:
        return "Statistics not found", 404

    if request.method == 'POST':
        points = request.form.get('points')
        rebounds = request.form.get('rebounds')
        assists = request.form.get('assists')
        turnovers = request.form.get('turnovers')
        minutes = request.form.get('minutes')

        if points and rebounds and assists and turnovers and minutes:
            cursor.execute('UPDATE Stats SET points = %s, rebounds = %s, assists = %s, turnovers = %s, minutes = %s WHERE stat_id = %s',
                           (points, rebounds, assists, turnovers, minutes, stat_id))
            conn.commit()
            flash('Statistics updated successfully!', 'success')
            return redirect(url_for('player_statistics', id=stat['player_id']))

    conn.close()
    return render_template('edit_statistics.html', stat=stat)

if __name__ == '__main__':
    app.run(debug=True)
