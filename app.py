from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import uuid

app = Flask(__name__)

# Connect to database
db = sqlite3.connect('database.db', check_same_thread=False)
# create a cursor
cursor = db.cursor()
# Create table for users
cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text, email text, unique_id text)""")


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', cur=cursor)


@app.route('/post/<int:post_id>')
def post(post_id):
    post_name = cursor.execute("SELECT title FROM posts WHERE id = ?", (post_id,)).fetchone()
    post_body = cursor.execute("SELECT body FROM posts WHERE id = ?", (post_id,)).fetchone()
    post_author = cursor.execute("SELECT author FROM posts WHERE id = ?", (post_id,)).fetchone()
    return render_template('post.html', post_id=post_id, cursor=cursor, post_name=post_name, post_body=post_body, post_author=post_author)


@app.route('/newpost')
def newpost():
    # check if user is logged in
    check_user = cursor.execute("SELECT * FROM users WHERE unique_id = ?", (request.cookies.get('unique_id'),)).fetchone()
    if check_user is None:
        return redirect(url_for('login'))

    return render_template('newpost.html')


@app.route('/newpost', methods=['POST'])
def newpost_post():
    # check if user is logged in

    check_user = cursor.execute("SELECT * FROM users WHERE unique_id = ?", (request.cookies.get('unique_id'),)).fetchone()
    if check_user:
        title = request.form['title']
        content = request.form['content']
        author = check_user[1]
        cursor.execute("INSERT INTO posts (title, body, author) VALUES (?, ?, ?)", (title, content, author))
        db.commit()
        return redirect(url_for('post', post_id=cursor.lastrowid))
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        # create a cookie for the user who contain his unique_id
        unique_id = user[4]
        resp = make_response(redirect(url_for('hello_world')))
        resp.set_cookie('unique_id', unique_id)
        return resp

    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('hello_world')))
    resp.set_cookie('user_id', '', expires=0)
    return resp


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    unique_id = str(uuid.uuid4()).encode('utf-8')
    cursor.execute("INSERT INTO users (username, password, email, unique_id) VALUES (?, ?, ?, ?)", (username, password, email, unique_id))
    db.commit()
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('unique_id', str(unique_id))
    return resp


if __name__ == '__main__':
    app.run()
