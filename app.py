from flask import Flask, request, jsonify
import requests
import os
import gunicorn
import psycopg2

app = Flask(__name__)

@app.route('/leads')
def get_leads():

    data = []

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    print("Querying Postgres...")
    cur.execute('SELECT * FROM "External Lead"', cur.rowcount)
    rows = cur.fetchall()

    for row in rows:

        print(row)
        data.append(row)

    return jsonify(data=data)

if __name__ == '__main__':
    app.run(debug=True)