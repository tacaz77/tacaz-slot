from flask import Flask, render_template, request, session, jsonify
import os

# Инициализация приложения с явным указанием папки шаблонов
app = Flask(__name__, template_folder='templates')

# Секретный ключ для работы сессий (баланса). 
# os.urandom(24) генерирует случайный ключ при каждом перезапуске сервера
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    # Устанавливаем стартовый баланс, если пользователь зашел впервые
    if 'balance' not in session:
        session['balance'] = 1000
    
    # Пытаемся отобразить главную страницу слота
    try:
        return render_template('index.html', balance=session['balance'])
    except Exception as e:
        return f"Ошибка: Файл index.html не найден в папке templates. Подробности: {e}", 404

@app.route('/spin', methods=['POST'])
def spin():
    # Получаем текущий баланс из сессии
    current_balance = session.get('balance', 1000)
    
    # Проверка: достаточно ли средств для ставки (ставка 100)
    if current_balance < 100:
        return jsonify({"error": "Недостаточно средств"}), 400
    
    # Списываем ставку и обновляем сессию
    session['balance'] = current_balance - 100
    return jsonify({"new_balance": session['balance']})

@app.route('/win', methods=['POST'])
def win():
    # Получаем данные о выигрыше от JavaScript
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "Неверные данные"}), 400
    
    win_amount = data.get('amount', 0)
    
    # Добавляем выигрыш к балансу
    current_balance = session.get('balance', 0)
    session['balance'] = current_balance + win_amount
    
    return jsonify({"new_balance": session['balance']})

if __name__ == '__main__':
    # Запуск приложения (на Render порт подставится автоматически через gunicorn)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
