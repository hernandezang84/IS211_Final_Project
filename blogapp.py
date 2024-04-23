from flask import Flask, request, url_for, redirect, render_template, session, g
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'blog.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row 
        return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    db = get_db()
    cur = db.execute('SELECT id, title FROM posts ORDER BY published_date DESC')
    posts = cur.fetchall()
    return render_template('home.html', posts=posts)

@app.route('/post/view/<int:post_id>')
def view_post(post_id):
    db = get_db()
    post = db.execute('SELECT id, title, content FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        abort(404)
    return render_template('view_post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        db = get_db()
       
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            
            if user['password'] == password:
                session['user_id'] = user['id']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password.')
        else:
           
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            
            
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']
    query = "SELECT id, title, content, published_date FROM posts WHERE user_id = ? ORDER BY published_date DESC"
    cur = db.execute('SELECT id, title, content, published_date FROM posts WHERE user_id = ? ORDER BY published_date DESC', (session['user_id'],))
    posts = db.execute('SELECT id, title, content, published_date FROM posts WHERE user_id = ? ORDER BY published_date DESC', (user_id,)).fetchall()    
    return render_template('dashboard.html', posts=posts)

@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO posts (title, content, published_date, user_id) VALUES (?, ?, ?, ?)',
                   [request.form['title'], request.form['content'], datetime.now(), session.get('user_id')])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_post.html')

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    db = get_db()
    if request.method == 'POST':
        db.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', 
                   [request.form['title'], request.form['content'], post_id])
        db.commit()
        return redirect('/dashboard')
    else:
        post = db.execute('SELECT title, content FROM posts WHERE id = ?', [post_id]).fetchone()
        return render_template('edit_post.html', post=post, post_id=post_id)

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', [post_id])
    db.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)