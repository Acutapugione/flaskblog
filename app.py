import sqlite3
from werkzeug.exceptions import abort
from flask import Flask, render_template, abort, request, url_for, flash, redirect
app = Flask(__name__)

app.config["SECRET_KEY"] = "BOBYKBOBYK777"

def get_db_connection():
    conn = sqlite3.connect('flask_blog/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
    (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.get('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    if posts == 0:
        return ("There is no posts yet")
    return render_template('index.html', posts=posts)

@app.get("/aboutblog")
def aboutblog():
    return render_template("aboutblog.html")

@app.get('/create')
def create():
    return render_template('create.html')

@app.post('/create')
def post_create():
    title = request.form.get('title')
    content = request.form.get('content')

    if not title:
        flash('Title is required!')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                     (title, content))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.get('/edit/<int:id>')
def edit(id):
    post = get_post(id)
    return render_template('edit.html', post=post)


@app.post('/edit')
def post_edit( ):
    title = request.form.get('title')
    content = request.form.get('content')
    post = get_post(id)
    if not title:
        flash('Title is required!')
    else:
        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ?  WHERE id = ?',
                     (title, content, id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

