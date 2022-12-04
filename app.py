import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
db_connection_count = 0
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post


# Function to get posts count
def get_posts_count():
    connection = get_db_connection()
    posts_count = connection.execute('SELECT count(*) as posts_count FROM posts WHERE 1').fetchone()
    connection.close()
    return posts_count

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key goes here'

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("app.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(logFormatter)
rootLogger.addHandler(stdout_handler)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(logFormatter)
rootLogger.addHandler(stderr_handler)

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    app.logger.info('Article list page successfull')
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info(f'Error 404 - can not find post id: {post_id}')
        return render_template('404.html'), 404
    else:
        app.logger.info(f'Article: "{post["title"]}" retrieved')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("The \"About Us\" page is retrieved.")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info(f'A new article is created: "{ title }".')

            return redirect(url_for('index'))

    return render_template('create.html')


# Define Healthcheck endpoint
@app.route('/healthz')
def abhealthzout():
    data = { "result": "OK - healthy"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Health check request successfull')
    return response

# Define Metrics endpoint
@app.route('/metrics')
def metrics():
    posts_count = get_posts_count()
    data = { "post_count": posts_count["posts_count"], "db_connection_count": db_connection_count }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Metrics request successfull')
    return response


# start the application on port 3111
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='3111')
