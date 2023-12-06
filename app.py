from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# DB init (SQLite)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER UNIQUE
    )
''')
conn.commit()
conn.close()

# HTTP POST
@app.route('/process_number', methods=['POST'])
def process_number():
    try:
        data = request.json
        number = data['number']

        # Connection to DB
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Проверка исключительной ситуации #1
        cursor.execute('SELECT * FROM numbers WHERE value = ?', (number,))
        existing_number = cursor.fetchone()
        if existing_number:
            conn.close()
            return jsonify({'error': 'Number already processed.'}), 400

        # Проверка исключительной ситуации #2
        cursor.execute('SELECT * FROM numbers WHERE value = ?', (number+1,))
        max_value = cursor.fetchone()
        if max_value is not None:
            conn.close()
            return jsonify({'error': 'Your number is 1 less than the existing one.'}), 400

        # Добавление числа в базу данных
        cursor.execute('INSERT INTO numbers (value) VALUES (?)', (number,))
        conn.commit()
        conn.close()

        # Возвращение увеличенного на единицу числа в ответе
        return jsonify({'result': number + 1})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Рендеринг HTML-страницы
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
