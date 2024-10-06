from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Sample data structure for questions
questions = {
    "Capital Access": [("Capital that represents the personal investment of the owner (or owners) of a company; sometimes called risk capital.", "Equity Capital", 100),
                ("The financing that an entrepreneur borrows and must repay with interest.", "Debt Capital", 200),("A method of raising equity capital in which a company sells shares of its stock to the general public for the first time.", "IPO", 300),("A method of raising capital that taps the power of social networking and allows entrepreneurs to post their elevator pitches and proposed investment terms on specialized Web sites and raise money from ordinary people who invest as little as $100.", "Crowdfunding", 400),("A process in which entrepreneurs tap their personal savings and use creative, low-cost start-up methods to launch their business.", "Bootstrapping", 500)],
    
    "Liquidity     ": [(" The meaning of credit score( connected to the Latin origin", "I believe score", 100),
             ("A financial statement that reports assets, liabilities, and owner's equity on a specific date.", "Balance Sheet", 200),("Time period that can pass before a customer's payment is due.", "Credit Period", 300),("The finance available for the day to day running of the business", "Working Capital", 400),("Long-term assets (e.g., patents, trademarks, copyrights) that have no real physical form but do have value", "Intangible Assets", 500)],
    
    "Asset Management" : [("Length of time a security has until maturity.", "Tenor", 100), ("Cash, government bonds or securities maturing within one business day.", "Daily Liquid Assets", 200), ("What is your name 2?", "Rachael", 200), ("The average maturity of all instruments, taken to the next interest reset date, by each security‘s percentage of total assets.", "Weighted Average Maturity", 300), ("The maximum time that a bond can be outstanding; the date when principal capital will be repaid.", "Maturity", 400), ("Average of the legal final maturity of all securities held in the portfolio, weighted by each security’s percentage of net assets.", "Weighted Average Life", 500)],
    
    "Citadel Fun Facts" : [("When was Citadel Founded?", "1990", 100), ("How many offices does Citadel have?","23", 200),("Where is Citadel headquarters located?", "Miami", 300),("What is Ken Griffin's favorite Fast Food Resturant?", "McDonalds", 400),("What is Ken Griffin's Zodiac Sign", "Libra", 500)],
    
    "Fun Facts About Us" : [("What is Michael's birthday?", "June 16th", 100), ("What is Rachael's birthday?", "December 30th", 200),("What is Michael's favorite food?", "Chicken Wings", 300),("What is Rachael's favorite food?", "Steak", 400),("Who is our favorite celebrity ", "Danny Devito", 500)]
    
}

@app.route('/')
@app.route('/index')
def index():
    if 'score' not in session:
        session['score'] = 0
    return render_template('index.html', questions=questions, score=session['score'])

@app.route('/home', methods=["GET", "POST"])
def home():
    if 'score' not in session:
        session['score'] = 0
    return render_template("home.html", questions=questions, score=session['score'])

@app.route('/question/<category>/<int:points>')
def question(category, points):
    question_data = next((q for q in questions[category] if q[2] == points), None)
    if question_data:
        return render_template('question.html', category=category, points=points, question=question_data[0])
    return redirect(url_for('home'))

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    category = request.form['category']
    points = int(request.form['points'])
    user_answer = request.form['answer']
    correct_answer = next((q[1] for q in questions[category] if q[2] == points), None)
    if user_answer.lower() == correct_answer.lower():
        session['score'] += points
        return redirect(url_for('correct', points=points, score=session['score']))
    else:
        session['score'] -= points
        return redirect(url_for('incorrect', points=-points, score=session['score'], correct_answer=correct_answer))

@app.route('/correct', methods=['GET','POST'])
def correct():
    points = request.args.get('points', 0, type=int)
    score = request.args.get('score', 0, type=int)
    return render_template('correct.html', points=points, score=score)

@app.route('/incorrect', methods=['GET', 'POST'])
def incorrect():
    points = request.args.get('points', 0, type=int)
    score = request.args.get('score', 0, type=int)
    correct_answer = request.args.get('correct_answer', '')
    return render_template('incorrect.html', points=points, score=score, correct_answer=correct_answer)


@app.route('/cap_access', methods=['GET','POST'])
def cap_access():
    return render_template('cap_access.html')

@app.route('/assetm', methods=['GET','POST'])
def assetm():
    print("we're in the assetm route???")
    return render_template('assetm.html')

@app.route('/li', methods=['GET','POST'])
def li():
    return render_template('li.html')

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')
if __name__ == '__main__': # runs code!!!!!
    app.run(host='0.0.0.0', port=81)




