import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

def db_connect():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    return connect

def get_post(post_id):
    connect = db_connect()
    post = connect.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connect.close()

    if post == None:
        abort(404)
    return post


@app.route('/')
def index():
    connection = db_connect()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    
    return render_template('index.html', posts=posts)



@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title required!')
        else:
            connect = db_connect()
            connect.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connect.commit()
            connect.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title required!')
        else:
            connect = db_connect()
            connect.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            connect.commit()
            connect.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    connect = db_connect()
    connect.execute('DELETE FROM posts WHERE id = ?', (id,))
    connect.commit()
    connect.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


app.run(host='0.0.0.0', port=81)