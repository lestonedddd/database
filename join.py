import mysql.connector
from flask import Blueprint, render_template

join_blueprint = Blueprint('join', __name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Password0206!',
        database='basketball'
    )
    return conn

@join_blueprint.route('/stats')
def stats():
    conn = get_db_connection()
    query = '''
        SELECT Player.name, Stats.points, Stats.rebounds, Stats.assists, Stats.turnovers, Stats.minutes, Game.date
        FROM Stats
        JOIN Player ON Stats.player_id = Player.player_id
        JOIN Game ON Stats.game_id = Game.game_id
    '''
    stats_data = conn.cursor(dictionary=True)
    stats_data.execute(query)
    results = stats_data.fetchall()
    conn.close()
    return render_template('template.html', stats=results)
