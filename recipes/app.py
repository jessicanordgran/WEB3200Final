import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for

PATH = 'db/recipe.sqlite'

app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')#login
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cookie')
def cookies():
    cookies = execute_sql('SELECT * FROM cookies')
    return render_template('cookie.html', cookies=cookies)

@app.route('/breakfast')
def breakfasts():
    breakfasts = execute_sql('SELECT * FROM breakfasts')
    return render_template('breakfast.html', breakfasts=breakfasts)

@app.route('/desert')
def deserts():
    deserts = execute_sql('SELECT * FROM deserts')
    return render_template('desert.html', deserts=deserts)

@app.route('/all')
def all():
    return render_template('all.html')

if __name__ == '__main__':
    app.run(debug=True)
