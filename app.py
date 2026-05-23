from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os
import random
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "quiz_secret_key_2024"

USER_FILE = "users.json"
RESULTS_FILE = "results.json"

# ─── Question Bank ────────────────────────────────────────────────────────────

QUESTION_BANK = {
    "software": [
        {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Processing Unit", "Central Program Unit", "Control Processing Unit"], "answer": "Central Processing Unit", "marks": 5},
        {"question": "Which language is used for web front-end development?", "options": ["Python", "HTML", "C++", "Java"], "answer": "HTML", "marks": 5},
        {"question": "Who developed Python?", "options": ["Dennis Ritchie", "James Gosling", "Guido van Rossum", "Elon Musk"], "answer": "Guido van Rossum", "marks": 10},
        {"question": "Which keyword defines a function in Python?", "options": ["function", "define", "def", "fun"], "answer": "def", "marks": 5},
        {"question": "Which symbol is used for single-line comments in Python?", "options": ["//", "#", "/* */", "--"], "answer": "#", "marks": 5},
        {"question": "Which company developed Windows OS?", "options": ["Apple", "Microsoft", "Google", "IBM"], "answer": "Microsoft", "marks": 5},
        {"question": "Which symbol ends a statement in C?", "options": [":", ";", ".", ","], "answer": ";", "marks": 5},
        {"question": "Which data type is used for decimals in Python?", "options": ["int", "str", "float", "bool"], "answer": "float", "marks": 5},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "High Text Machine Language", "Hyper Tool Multi Language", "Hyper Transfer Markup Language"], "answer": "Hyper Text Markup Language", "marks": 5},
        {"question": "Which HTML tag inserts an image?", "options": ["<image>", "<img>", "<pic>", "<src>"], "answer": "<img>", "marks": 5},
        {"question": "CSS stands for?", "options": ["Computer Style Sheets", "Creative Style Sheets", "Cascading Style Sheets", "Colorful Style Sheets"], "answer": "Cascading Style Sheets", "marks": 5},
        {"question": "Which keyword loops in Python?", "options": ["repeat", "loop", "for", "iterate"], "answer": "for", "marks": 5},
        {"question": "Which function prints output in Python?", "options": ["echo()", "display()", "print()", "show()"], "answer": "print()", "marks": 5},
        {"question": "Which protocol is used by websites?", "options": ["FTP", "HTTP", "SMTP", "TCP"], "answer": "HTTP", "marks": 5},
        {"question": "Which device inputs text?", "options": ["Monitor", "Keyboard", "Printer", "Speaker"], "answer": "Keyboard", "marks": 5},
        {"question": "What is the file extension of Python files?", "options": [".py", ".java", ".html", ".cpp"], "answer": ".py", "marks": 5},
        {"question": "Which statement makes decisions in Python?", "options": ["loop", "if", "switch", "case"], "answer": "if", "marks": 5},
        {"question": "Which memory is temporary in a computer?", "options": ["ROM", "RAM", "Hard Disk", "SSD"], "answer": "RAM", "marks": 5},
        {"question": "Which keyword creates a class in Python?", "options": ["object", "class", "define", "struct"], "answer": "class", "marks": 10},
        {"question": "Which company developed Android?", "options": ["Apple", "Google", "Microsoft", "Samsung"], "answer": "Google", "marks": 5},
        {"question": "Which operator compares values in Python?", "options": ["==", "=", "+=", "//"], "answer": "==", "marks": 5},
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "System Query Logic", "Structured Quick Language"], "answer": "Structured Query Language", "marks": 5},
        {"question": "Which of these is a version control system?", "options": ["Docker", "Git", "Linux", "Apache"], "answer": "Git", "marks": 5},
        {"question": "What does API stand for?", "options": ["Application Programming Interface", "Applied Program Input", "Automated Protocol Interface", "Application Process Input"], "answer": "Application Programming Interface", "marks": 5},
        {"question": "Which data structure uses LIFO order?", "options": ["Queue", "Stack", "Array", "Linked List"], "answer": "Stack", "marks": 10},
    ],
    "general": [
        {"question": "What is the capital of India?", "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"], "answer": "Delhi", "marks": 5},
        {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"], "answer": "7", "marks": 5},
        {"question": "Which is the largest ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific", "marks": 5},
        {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "Mars", "marks": 5},
        {"question": "Who invented the telephone?", "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Marconi"], "answer": "Alexander Graham Bell", "marks": 5},
        {"question": "What is the chemical symbol for water?", "options": ["O2", "CO2", "H2O", "NaCl"], "answer": "H2O", "marks": 5},
        {"question": "Which is the largest country by area?", "options": ["China", "USA", "Canada", "Russia"], "answer": "Russia", "marks": 5},
        {"question": "How many days are in a leap year?", "options": ["364", "365", "366", "367"], "answer": "366", "marks": 5},
        {"question": "Which is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": "Nile", "marks": 5},
        {"question": "What is the speed of light (approx)?", "options": ["3×10⁵ km/s", "3×10⁶ km/s", "3×10⁴ km/s", "3×10³ km/s"], "answer": "3×10⁵ km/s", "marks": 10},
        {"question": "Who wrote Romeo and Juliet?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "answer": "William Shakespeare", "marks": 5},
        {"question": "Which gas do plants absorb?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": "Carbon Dioxide", "marks": 5},
        {"question": "Which is the smallest planet in our solar system?", "options": ["Venus", "Mars", "Mercury", "Pluto"], "answer": "Mercury", "marks": 5},
        {"question": "Who painted the Mona Lisa?", "options": ["Picasso", "Van Gogh", "Leonardo da Vinci", "Raphael"], "answer": "Leonardo da Vinci", "marks": 5},
        {"question": "What is the capital of France?", "options": ["Rome", "Berlin", "Madrid", "Paris"], "answer": "Paris", "marks": 5},
        {"question": "Which element has the symbol 'O'?", "options": ["Gold", "Silver", "Oxygen", "Osmium"], "answer": "Oxygen", "marks": 5},
        {"question": "How many bones are in the adult human body?", "options": ["196", "206", "216", "186"], "answer": "206", "marks": 5},
        {"question": "What is the capital of Japan?", "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "answer": "Tokyo", "marks": 5},
        {"question": "Which is the largest mammal?", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], "answer": "Blue Whale", "marks": 5},
        {"question": "In which year did World War II end?", "options": ["1943", "1944", "1945", "1946"], "answer": "1945", "marks": 5},
        {"question": "What is H2O commonly known as?", "options": ["Salt Water", "Water", "Hydrogen Gas", "Oxygen Gas"], "answer": "Water", "marks": 5},
        {"question": "Which country has the most population?", "options": ["India", "USA", "China", "Indonesia"], "answer": "India", "marks": 5},
        {"question": "Mount Everest is located in which country?", "options": ["India", "China", "Nepal", "Tibet"], "answer": "Nepal", "marks": 5},
        {"question": "What is the national sport of India?", "options": ["Cricket", "Hockey", "Kabaddi", "Football"], "answer": "Hockey", "marks": 5},
        {"question": "Which planet is closest to the Sun?", "options": ["Venus", "Earth", "Mercury", "Mars"], "answer": "Mercury", "marks": 5},
    ],
    "cricket": [
        {"question": "How many players are there in a cricket team?", "options": ["9", "10", "11", "12"], "answer": "11", "marks": 5},
        {"question": "Which country won the first ICC Cricket World Cup (1975)?", "options": ["India", "Australia", "West Indies", "England"], "answer": "West Indies", "marks": 10},
        {"question": "Who holds the record for most Test centuries?", "options": ["Ricky Ponting", "Brian Lara", "Sachin Tendulkar", "Virat Kohli"], "answer": "Sachin Tendulkar", "marks": 10},
        {"question": "What is the maximum number of overs in an ODI?", "options": ["40", "45", "50", "60"], "answer": "50", "marks": 5},
        {"question": "Which country invented cricket?", "options": ["Australia", "India", "England", "South Africa"], "answer": "England", "marks": 5},
        {"question": "What is a 'duck' in cricket?", "options": ["A catch", "Score of zero", "A wide ball", "A no-ball"], "answer": "Score of zero", "marks": 5},
        {"question": "Who is known as the 'God of Cricket'?", "options": ["Virat Kohli", "MS Dhoni", "Sachin Tendulkar", "Sourav Ganguly"], "answer": "Sachin Tendulkar", "marks": 5},
        {"question": "How many stumps are in a cricket wicket?", "options": ["2", "3", "4", "5"], "answer": "3", "marks": 5},
        {"question": "Which country hosts the IPL?", "options": ["England", "Australia", "India", "UAE"], "answer": "India", "marks": 5},
        {"question": "What does LBW stand for in cricket?", "options": ["Leg Before Wicket", "Left Behind Wicket", "Leg Ball Wide", "Left Bat Wide"], "answer": "Leg Before Wicket", "marks": 5},
        {"question": "Who scored the first double century in ODI cricket?", "options": ["Virat Kohli", "Rohit Sharma", "Sachin Tendulkar", "Martin Guptill"], "answer": "Sachin Tendulkar", "marks": 10},
        {"question": "In which year did India win the ICC T20 World Cup for the first time?", "options": ["2005", "2007", "2009", "2011"], "answer": "2007", "marks": 10},
        {"question": "Who captained India to win the 2011 Cricket World Cup?", "options": ["Sourav Ganguly", "Rahul Dravid", "MS Dhoni", "Virat Kohli"], "answer": "MS Dhoni", "marks": 5},
        {"question": "What is the highest individual score in Test cricket?", "options": ["375", "400", "501*", "365"], "answer": "400", "marks": 10},
        {"question": "How many runs does a 'six' score in cricket?", "options": ["4", "5", "6", "7"], "answer": "6", "marks": 5},
        {"question": "Which bowler has the most wickets in Test cricket?", "options": ["Anil Kumble", "Shane Warne", "Muttiah Muralitharan", "Glenn McGrath"], "answer": "Muttiah Muralitharan", "marks": 10},
        {"question": "What is the pink ball Test match associated with?", "options": ["Day matches", "Day-night matches", "Indoor matches", "Women cricket"], "answer": "Day-night matches", "marks": 5},
        {"question": "Which trophy is awarded in Test series between India and Australia?", "options": ["Ashes Trophy", "Border-Gavaskar Trophy", "Freedom Trophy", "Pataudi Trophy"], "answer": "Border-Gavaskar Trophy", "marks": 5},
        {"question": "What is a 'hat-trick' in cricket?", "options": ["Three sixes in a row", "Three wickets in three balls", "Three fours in an over", "Three wides in a row"], "answer": "Three wickets in three balls", "marks": 5},
        {"question": "Which format of cricket has the fewest overs per side?", "options": ["Test", "ODI", "T20", "T10"], "answer": "T10", "marks": 5},
        {"question": "Who holds the IPL record for most runs in a single season?", "options": ["Virat Kohli", "David Warner", "Brendon McCullum", "AB de Villiers"], "answer": "Virat Kohli", "marks": 10},
        {"question": "What is 'Chinaman' bowling?", "options": ["Off-spin by left-hander", "Left-arm unorthodox spin", "Right-arm leg spin", "Fast bowling"], "answer": "Left-arm unorthodox spin", "marks": 10},
        {"question": "Which fielding position is directly behind the batsman?", "options": ["Slip", "Gully", "Point", "Fine Leg"], "answer": "Fine Leg", "marks": 5},
        {"question": "How many balls are in one over in cricket?", "options": ["4", "5", "6", "8"], "answer": "6", "marks": 5},
        {"question": "Which stadium has the highest capacity for cricket?", "options": ["Eden Gardens", "MCG", "Narendra Modi Stadium", "Wankhede"], "answer": "Narendra Modi Stadium", "marks": 5},
    ]
}

CATEGORY_INFO = {
    "software": {"name": "Software & Technology", "icon": "💻", "color": "#6366f1"},
    "general": {"name": "General Knowledge", "icon": "🌍", "color": "#10b981"},
    "cricket": {"name": "Cricket", "icon": "🏏", "color": "#f59e0b"},
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path, default={}):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

def get_questions_for_session(category, user_email):
    """Shuffle questions per sign-in session using email+timestamp seed."""
    pool = QUESTION_BANK.get(category, [])
    seed = hash(user_email + str(session.get('login_time', '')))
    rng = random.Random(seed)
    shuffled = pool[:]
    rng.shuffle(shuffled)
    return shuffled[:20]

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm', '').strip()

        if not is_valid_email(email):
            error = "Please enter a valid email address."
        elif not name:
            error = "Full name is required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."
        else:
            users = load_json(USER_FILE, {})
            if email in users:
                error = "An account with this email already exists."
            else:
                users[email] = {
                    "name": name,
                    "password": password,
                    "avatar": name[0].upper(),
                    "joined": datetime.now().strftime("%d %b %Y")
                }
                save_json(USER_FILE, users)
                return redirect('/login?registered=1')

    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    registered = request.args.get('registered')
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not is_valid_email(email):
            error = "Please enter a valid email address."
        else:
            users = load_json(USER_FILE, {})
            if email in users and users[email]['password'] == password:
                session['user'] = email
                session['login_time'] = datetime.now().isoformat()
                return redirect('/dashboard')
            else:
                error = "Invalid email or password."

    return render_template('login.html', error=error, registered=registered)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    users = load_json(USER_FILE, {})
    user_data = users.get(session['user'], {})
    results = load_json(RESULTS_FILE, {})
    user_results = results.get(session['user'], [])

    # Stats
    total_quizzes = len(user_results)
    best_pct = 0
    cat_stats = {c: {"taken": 0, "total_score": 0, "total_max": 0} for c in QUESTION_BANK}
    recent = []
    for r in user_results:
        cat = r.get('category', 'general')
        pct = (r['score'] / r['total'] * 100) if r['total'] > 0 else 0
        if pct > best_pct:
            best_pct = pct
        if cat in cat_stats:
            cat_stats[cat]['taken'] += 1
            cat_stats[cat]['total_score'] += r['score']
            cat_stats[cat]['total_max'] += r['total']
    recent = list(reversed(user_results[-5:]))

    return render_template('dashboard.html',
        user=user_data,
        email=session['user'],
        total_quizzes=total_quizzes,
        best_pct=round(best_pct, 1),
        cat_stats=cat_stats,
        cat_info=CATEGORY_INFO,
        recent=recent,
    )

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect('/login')
    users = load_json(USER_FILE, {})
    user_data = users.get(session['user'], {})
    message = None
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        current_pw = request.form.get('current_password', '').strip()
        new_pw = request.form.get('new_password', '').strip()
        confirm_pw = request.form.get('confirm_password', '').strip()

        if name:
            user_data['name'] = name
            user_data['avatar'] = name[0].upper()

        if current_pw or new_pw:
            if user_data['password'] != current_pw:
                error = "Current password is incorrect."
            elif len(new_pw) < 6:
                error = "New password must be at least 6 characters."
            elif new_pw != confirm_pw:
                error = "Passwords do not match."
            else:
                user_data['password'] = new_pw
                message = "Profile updated successfully!"

        if not error:
            users[session['user']] = user_data
            save_json(USER_FILE, users)
            if not message:
                message = "Profile updated successfully!"

    return render_template('profile.html', user=user_data, email=session['user'], message=message, error=error)

@app.route('/select')
def select_category():
    if 'user' not in session:
        return redirect('/login')
    return render_template('select.html', categories=CATEGORY_INFO)

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect('/login')
    category = request.args.get('category', 'general')
    if category not in QUESTION_BANK:
        return redirect('/select')
    questions = get_questions_for_session(category, session['user'])
    session['current_category'] = category
    return render_template('quiz.html', questions=questions, category=category, cat_info=CATEGORY_INFO[category])

@app.route('/result', methods=['POST'])
def result():
    if 'user' not in session:
        return redirect('/login')

    category = session.get('current_category', 'general')
    questions = get_questions_for_session(category, session['user'])

    score = 0
    total_marks = sum(q['marks'] for q in questions)
    details = []

    for i, q in enumerate(questions):
        selected = request.form.get(f'q{i}')
        correct = selected == q['answer']
        if correct:
            score += q['marks']
        elif selected:
            score -= 1
        details.append({
            "question": q['question'],
            "selected": selected,
            "answer": q['answer'],
            "marks": q['marks'],
            "correct": correct,
        })

    pct = round(score / total_marks * 100, 1) if total_marks > 0 else 0

    # Save result
    results = load_json(RESULTS_FILE, {})
    if session['user'] not in results:
        results[session['user']] = []
    results[session['user']].append({
        "category": category,
        "score": score,
        "total": total_marks,
        "pct": pct,
        "date": datetime.now().strftime("%d %b %Y, %H:%M"),
    })
    save_json(RESULTS_FILE, results)

    users = load_json(USER_FILE, {})
    user_data = users.get(session['user'], {})

    return render_template('result.html',
        score=score, total=total_marks, pct=pct,
        details=details, category=category,
        cat_info=CATEGORY_INFO[category],
        user=user_data,
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
