from flask import Flask, render_template, request, redirect, url_for
from flask import g
import sqlite3

app = Flask(__name__)

def get_db():
    fruits = g.cursor.execute('select * from fruits')
    fruits = fruits.fetchall()
    fruits = [fruit[0] for fruit in fruits]
    return fruits

@app.before_request
def before_request():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect('database.db')
        g.cursor = g.db.cursor()

    
with app.app_context():
    before_request()
    get_db()

@app.teardown_appcontext
def teardown_context(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    fruits = get_db()
    print(g)
    if not hasattr(g,'shoppinglist'):
        g.shoppinglist = ['abc']
    if request.method == 'POST':
        fruit_selected = request.form['fruits_select']
        print(g.shoppinglist)
        g.shoppinglist.append(fruit_selected)
        print(g.shoppinglist)
    return render_template('fruits.html', fruits=fruits, shoppinglist=g.shoppinglist)
        
        

if __name__ == '__main__':
    app.run(debug=True)