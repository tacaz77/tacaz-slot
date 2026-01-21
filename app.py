from flask import Flask, render_template, request, session, jsonify
import os

app = Flask(__name__)
# Секретный ключ обязателен для работы баланса (сессий)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    # Устанавливаем баланс, если его нет
    if 'balance' not in session:
        session['balance'] = 1000
    return render_template('index.html', balance=session['balance'])

@app.route('/spin', methods=['POST'])
def spin():
    # Проверяем баланс перед началом
    current_balance = session.get('balance', 1000)
    if current_balance < 100:
        return jsonify({"error": "Low balance"}), 400
    
    # Списываем ставку и сохраняем
    session['balance'] = current_balance - 100
    return jsonify({"new_balance": session['balance']})

@app.route('/win', methods=['POST'])
def win():
    # Получаем сумму выигрыша из JS
    data = request.get_json()
    amount = data.get('amount', 0)
    
    # Добавляем к текущему балансу и сохраняем
    current_balance = session.get('balance', 0)
    session['balance'] = current_balance + amount
    return jsonify({"new_balance": session['balance']})

if __name__ == '__main__':
    app.run()

