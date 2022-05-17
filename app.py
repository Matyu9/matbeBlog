from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Connect to database
db = mysql.connector.connect(host="localhost", user="mathieu", passwd="SecureMDP123456", database="blog")
# create a cursor
cursor = db.cursor()


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', cur=cursor)

### CREATE TABLE posts (   id INTEGER PRIMARY KEY AUTO_INCREMENT,   title TEXT,   body TEXT );

if __name__ == '__main__':
    app.run()
