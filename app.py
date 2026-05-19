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
    },

    # Additional Questions

    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Processing Unit",
            "Central Program Unit",
            "Control Processing Unit"
        ],
        "answer": "Central Processing Unit",
        "marks": 5
    },
    {
        "question": "Which company developed Windows?",
        "options": ["Apple", "Microsoft", "Google", "IBM"],
        "answer": "Microsoft",
        "marks": 5
    },
    {
        "question": "Which symbol is used to end a statement in C language?",
        "options": [":", ";", ".", ","],
        "answer": ";",
        "marks": 5
    },
    {
        "question": "Which data type is used for decimal values in Python?",
        "options": ["int", "str", "float", "bool"],
        "answer": "float",
        "marks": 5
    },
    {
        "question": "HTML stands for?",
        "options": [
            "Hyper Text Markup Language",
            "High Text Machine Language",
            "Hyper Tool Multi Language",
            "Hyper Transfer Markup Language"
        ],
        "answer": "Hyper Text Markup Language",
        "marks": 5
    },
    {
        "question": "Which tag is used to insert an image in HTML?",
        "options": ["<image>", "<img>", "<pic>", "<src>"],
        "answer": "<img>",
        "marks": 5
    },
    {
        "question": "Which operator is used for addition in Python?",
        "options": ["*", "+", "/", "%"],
        "answer": "+",
        "marks": 5
    },
    {
        "question": "CSS stands for?",
        "options": [
            "Computer Style Sheets",
            "Creative Style Sheets",
            "Cascading Style Sheets",
            "Colorful Style Sheets"
        ],
        "answer": "Cascading Style Sheets",
        "marks": 5
    },
    {
        "question": "Which keyword is used for loop in Python?",
        "options": ["repeat", "loop", "for", "iterate"],
        "answer": "for",
        "marks": 5
    },
    {
        "question": "Which function is used to display output in Python?",
        "options": ["echo()", "display()", "print()", "show()"],
        "answer": "print()",
        "marks": 5
    },
    {
        "question": "Which protocol is used for websites?",
        "options": ["FTP", "HTTP", "SMTP", "TCP"],
        "answer": "HTTP",
        "marks": 5
    },
    {
        "question": "Which device is used to input text?",
        "options": ["Monitor", "Keyboard", "Printer", "Speaker"],
        "answer": "Keyboard",
        "marks": 5
    },
    {
        "question": "Which one is a programming language?",
        "options": ["Python", "HTML", "CSS", "Photoshop"],
        "answer": "Python",
        "marks": 5
    },
    {
        "question": "What is the extension of Python files?",
        "options": [".py", ".java", ".html", ".cpp"],
        "answer": ".py",
        "marks": 5
    },
    {
        "question": "Which statement is used to make decisions in Python?",
        "options": ["loop", "if", "switch", "case"],
        "answer": "if",
        "marks": 5
    },
    {
        "question": "Which HTML tag is used for headings?",
        "options": ["<p>", "<h1>", "<title>", "<head>"],
        "answer": "<h1>",
        "marks": 5
    },
    {
        "question": "Which memory is temporary in computer?",
        "options": ["ROM", "RAM", "Hard Disk", "SSD"],
        "answer": "RAM",
        "marks": 5
    },
    {
        "question": "Which symbol is used for multiplication in Python?",
        "options": ["x", "*", "%", "#"],
        "answer": "*",
        "marks": 5
    },
    {
        "question": "Which keyword is used to create a class in Python?",
        "options": ["object", "class", "define", "struct"],
        "answer": "class",
        "marks": 10
    },
    {
        "question": "Which company developed Android?",
        "options": ["Apple", "Google", "Microsoft", "Samsung"],
        "answer": "Google",
        "marks": 5
    },
    {
        "question": "Which operator is used for comparison in Python?",
        "options": ["==", "=", "+=", "//"],
        "answer": "==",
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