from flask import Flask, render_template, request, session, jsonify
import os

app = Flask(__name__)
app.secret_key = 'slot_secret_key_2026'

@app.route('/')
def index():
    if 'balance' not in session:
        session['balance'] = 1000  # Стартовый капитал
    return render_template('index.html', balance=session['balance'])

@app.route('/spin', methods=['POST'])
def spin():
    bet = 100
    if session.get('balance', 0) < bet:
        return jsonify({"error": "Low balance"}), 400
    
    session['balance'] -= bet
    # В будущем здесь можно добавить серверную проверку RNG
    return jsonify({"new_balance": session['balance']})

@app.route('/win', methods=['POST'])
def win():
    amount = request.json.get('amount', 0)
    session['balance'] += amount
    return jsonify({"new_balance": session['balance']})

if __name__ == '__main__':
    app.run(debug=True)
