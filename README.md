# Project Structure
    ecommerce-app/
    │   Dockerfile
    │   main.py
    │   requirements.txt
    └───templates/
            │   index.html
            │   add_product.html










# Flask-App Container
## Install Dependencies
    sudo dnf install -y podman podman-compose python3 python3-pip
    '
## Set Up the Project Directory
    mkdir -p ecommerce-app/app/templates
    cd ecommerce-app

## Create the Dockerfile
    # Use the official Python image
    FROM python:3.9-slim
    
    # Set the working directory
    WORKDIR /app
    
    # Copy application files
    COPY . .
    
    # Install dependencies
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Expose the port
    EXPOSE 5000
    
    # Start the Flask application
    CMD ["python3", "main.py"]

## Create main.py
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

## Create requirements.txt
    Insert:5
    
    Flask==2.3.2
    psycopg2-binary==2.9.6
## Build the Flask App Image
    podman build -t ecommerce-web -f Dockerfile .

## Run the Flask App Container
    podman run -d \
      --name ecommerce-web \
      -p 5000:5000 \
      --env DB_HOST=host.containers.internal \
      --env DB_NAME=ecommerce \
      --env DB_USER=postgres \
      --env DB_PASSWORD=postgres \
      ecommerce-web

# PostgreSQL Container
## Create & Run PostgrSQL Container
    podman run -d \
      --name ecommerce-db \
      -e POSTGRES_DB=ecommerce \
      -e POSTGRES_USER=postgres \
      -e POSTGRES_PASSWORD=postgres \
      -v ecommerce-data:/var/lib/postgresql/data \
      -p 5432:5432 \
      postgres:14-alpine

## Add Table to the Database
    podman exec -it ecommerce-db psql -U postgres -d ecommerce

    CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price NUMERIC
    );

# Access the Web
    podman logs ecommerce-web



    
