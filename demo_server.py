#!/usr/bin/env python3
"""
Demo Flask Server for Smoke Testing
Mô phỏng một ứng dụng Microblog đơn giản để test
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
import json

app = Flask(__name__)
app.secret_key = 'demo_secret_key_for_testing'

# In-memory storage for demo
users = {}
posts = []

# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Demo Microblog</title></head>
<body>
    <h1>Welcome to Demo Microblog</h1>
    {% if session.get('username') %}
        <p>Hello, {{ session.username }}!</p>
        <form method="POST" action="/">
            <textarea name="post" placeholder="What's on your mind?" required></textarea><br>
            <button type="submit" name="submit">Submit</button>
        </form>
        <p><a href="/auth/logout">Logout</a></p>
    {% else %}
        <p><a href="/auth/login">Login</a> | <a href="/auth/register">Register</a></p>
    {% endif %}
    
    <h2>Recent Posts</h2>
    {% for post in posts %}
        <div style="border:1px solid #ccc; margin:10px; padding:10px;">
            <strong>{{ post.username }}:</strong> {{ post.content }}
        </div>
    {% endfor %}
    
    <p><a href="/explore">Explore</a></p>
</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Login - Demo Microblog</title></head>
<body>
    <h1>Login</h1>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <input type="checkbox" name="remember_me"> Remember me<br><br>
        <button type="submit" name="submit">Sign In</button>
    </form>
    <p><a href="/auth/register">Don't have an account? Register here</a></p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
'''

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Register - Demo Microblog</title></head>
<body>
    <h1>Register</h1>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="email" name="email" placeholder="Email" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <input type="password" name="password2" placeholder="Repeat Password" required><br><br>
        <button type="submit" name="submit">Register</button>
    </form>
    <p><a href="/auth/login">Already have an account? Login here</a></p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
'''

EXPLORE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Explore - Demo Microblog</title></head>
<body>
    <h1>Explore Posts</h1>
    {% for post in posts %}
        <div style="border:1px solid #ccc; margin:10px; padding:10px;">
            <strong>{{ post.username }}:</strong> {{ post.content }}
        </div>
    {% endfor %}
    <p><a href="/">Back to Home</a></p>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if session.get('username'):
            content = request.form.get('post')
            if content:
                posts.append({
                    'username': session['username'],
                    'content': content
                })
        return redirect(url_for('index'))
    
    return render_template_string(HOME_TEMPLATE, posts=posts[:10])

@app.route('/index')
def index_alt():
    return redirect(url_for('index'))

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template_string(LOGIN_TEMPLATE + '<p style="color:red;">Invalid credentials</p>')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        if password != password2:
            return render_template_string(REGISTER_TEMPLATE + '<p style="color:red;">Passwords do not match</p>')
        
        if username in users:
            return render_template_string(REGISTER_TEMPLATE + '<p style="color:red;">Username already exists</p>')
        
        users[username] = {
            'email': email,
            'password': password
        }
        
        return redirect(url_for('login'))
    
    return render_template_string(REGISTER_TEMPLATE)

@app.route('/auth/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/explore')
def explore():
    return render_template_string(EXPLORE_TEMPLATE, posts=posts)

# API Endpoints
@app.route('/api')
def api_root():
    return jsonify({
        'message': 'Demo Microblog API',
        'version': '1.0',
        'endpoints': ['/api/users', '/api/tokens']
    })

@app.route('/api/users')
def api_users():
    # Simulate authentication requirement
    if 'Authorization' in request.headers:
        return jsonify({
            'users': [{'username': user, 'email': data['email']} for user, data in users.items()]
        })
    else:
        return jsonify({'error': 'Authentication required'}), 401

@app.route('/api/tokens', methods=['POST'])
def api_tokens():
    # Simulate token endpoint
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
        
    username = data.get('username')
    password = data.get('password')
    
    if username and password and username in users and users[username]['password'] == password:
        return jsonify({'token': f'demo_token_{username}'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/tokens', methods=['GET'])
def api_tokens_get():
    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/api/nonexistent')
def api_nonexistent():
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Demo Microblog Server...")
    print("📝 Default test user will be created: testuser/password123")
    
    # Create a default test user
    users['testuser'] = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    
    # Add some sample posts
    posts.append({
        'username': 'testuser',
        'content': 'Welcome to the demo microblog!'
    })
    
    print("🌐 Server will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(host='localhost', port=5000, debug=True, use_reloader=False)
