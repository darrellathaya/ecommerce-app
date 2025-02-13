from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'ecommerce'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products;')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO products (name, description, price) VALUES (%s, %s, %s)',
                    (name, description, price))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
