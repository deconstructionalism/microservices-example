from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)
conn = sqlite3.connect('owners.db')

c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='owners'")
owners_exists = c.fetchone()
if not owners_exists:
    c.execute('''
    CREATE TABLE owners 
    (id INTEGER PRIMARY KEY, date DATETIME, first_name TEXT, last_name TEXT, phone_number TEXT, area_code TEXT) 
    ''')

    c.execute('''
    INSERT INTO owners (first_name, last_name, phone_number, area_code) VALUES ("Joe", "Biden", "666-777-9999", "90210")
    ''')
    conn.commit()

cols = ('id', 'date', 'first_name', 'last_name', 'phone_number', 'area_code')


@app.route('/owners', methods=['GET'])
def index_owners():
    c.execute('SELECT * FROM owners')
    vals = c.fetchall()
    print(vals)
    return_list = [dict(zip(cols, val)) for val in vals]    
    return jsonify(return_list)

@app.route('/owners/<int:owner_id>', methods=['GET'])
def show_owners(owner_id):
    c.execute('SELECT * FROM owners WHERE id=?', str(owner_id))
    val = c.fetchone()
    return_dict = dict(zip(cols, val))
    return jsonify(return_dict)


@app.route('/owners', methods=['POST'])
def create_owner():
    params = request.form
    print(params)
    c.execute('INSERT INTO owners (first_name, last_name, phone_number, area_code) VALUES (?, ?, ?, ?)', [params['first_name'], params['last_name'], params['phone_number'], params['area_code']])
    conn.commit()
    c.execute('SELECT * FROM owners ORDER BY id DESC LIMIT 1')
    val = c.fetchone()
    return_dict = dict(zip(cols, val))
    return jsonify(return_dict)

@app.route('/owners/<int:owner_id>', methods=['DELETE'])
def destroy_owner(owner_id):
    c.execute('DELETE FROM owners WHERE id=?', str(owner_id))
    conn.commit()
    return '{} DELETED'.format(owner_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)