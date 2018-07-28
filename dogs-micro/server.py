from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)
conn = sqlite3.connect('dogs.db')

c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dogs'")
dogs_exists = c.fetchone()
if not dogs_exists:
    c.execute('''
    CREATE TABLE dogs 
    (id INTEGER PRIMARY KEY, date DATETIME, breed TEXT, age INTEGER, name TEXT, owner_ref INTEGER) 
    ''')

    c.execute('''
    INSERT INTO dogs (name, owner_ref, age, breed) VALUES ("Fido", 1, 3, "Rottweiler")
    ''')
    conn.commit()

cols = ('id', 'date', 'breed', 'age', 'name', 'owner_ref')


@app.route('/dogs', methods=['GET'])
def index_dogs():
    c.execute('SELECT * FROM dogs')
    return_list = [dict(zip(cols, val)) for val in c.fetchall()]    
    return jsonify(return_list)

@app.route('/dogs/<int:dog_id>', methods=['GET'])
def show_dogs(dog_id):
    c.execute('SELECT * FROM dogs WHERE id=?', str(dog_id))
    return_dict = dict(zip(cols, c.fetchone()))
    return jsonify(return_dict)

@app.route('/dogs', methods=['POST'])
def create_dog():
    params = request.form
    c.execute('INSERT INTO dogs (name, owner_ref, age, breed) VALUES (?, ?, ?, ?)', [params['name'], params['owner_ref'], params['age'], params['breed']])
    conn.commit()
    c.execute('SELECT * FROM dogs ORDER BY id DESC LIMIT 1')
    return_dict = dict(zip(cols, c.fetchone()))
    return jsonify(return_dict)

@app.route('/dogs/<int:dog_id>', methods=['DELETE'])
def destroy_dog(dog_id):
    c.execute('DELETE FROM dogs WHERE id=?', str(dog_id))
    conn.commit()
    return '{} DELETED'.format(dog_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)