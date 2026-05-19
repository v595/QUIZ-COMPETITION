from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# Quiz Questions
questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "answer": "Delhi",
        "marks": 5
    },
    {
        "question": "Which language is used for web development?",
        "options": ["Python", "HTML", "C++", "Java"],
        "answer": "HTML",
        "marks": 5
    },
    {
        "question": "Who developed Python?",
        "options": [
            "Dennis Ritchie",
            "James Gosling",
            "Guido van Rossum",
            "Elon Musk"
        ],
        "answer": "Guido van Rossum",
        "marks": 10
    },
    {
        "question": "Which keyword is used for function in Python?",
        "options": ["function", "define", "def", "fun"],
        "answer": "def",
        "marks": 5
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/* */", "--"],
        "answer": "#",
        "marks": 5
    }
]

# User File
USER_FILE = "users.json"

# Create users.json if not exists
if not os.path.exists(USER_FILE):

    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# Home
@app.route('/')
def home():

    if 'user' in session:
        return redirect('/dashboard')

    return redirect('/login')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        with open(USER_FILE, "r") as f:
            users = json.load(f)

        # Check existing user
        if username in users:
            return "User already exists!"

        # Save new user
        users[username] = password

        with open(USER_FILE, "w") as f:
            json.dump(users, f)

        return redirect('/login')

    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        with open(USER_FILE, "r") as f:
            users = json.load(f)

        if username in users and users[username] == password:

            session['user'] = username

            return redirect('/dashboard')

        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():

    # Login required
    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html')

# Quiz Page
@app.route('/quiz')
def quiz():

    # Login required
    if 'user' not in session:
        return redirect('/login')

    return render_template(
        'quiz.html',
        questions=questions
    )

# Result Page
@app.route('/result', methods=['POST'])
def result():

    if 'user' not in session:
        return redirect('/login')

    score = 0
    total_marks = 0

    for i, q in enumerate(questions):

        total_marks += q['marks']

        selected = request.form.get(f'q{i}')

        # Correct Answer
        if selected == q['answer']:

            score += q['marks']

        # Negative Marking
        elif selected is not None:

            score -= 1

    return render_template(
        'result.html',
        score=score,
        total=total_marks
    )

# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')

# Run App
if __name__ == '__main__':
    app.run(debug=True)