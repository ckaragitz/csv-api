from flask import Flask, request, jsonify, make_response
import gunicorn
import requests
import os
import io
import csv
import psycopg2

app = Flask(__name__)

@app.route('/leads', methods=["POST"])
def post_leads():

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    f = request.files['file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream)
    next(reader)

    for row in reader:
        print(row)
        cur.execute(
        'INSERT INTO "External Lead" VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
        (row,)
        )

    conn.commit()

    #cur.copy_from(stream, '"External Lead"', sep=',')

    stream.seek(0)
    result = stream.read()

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

if __name__ == '__main__':
    app.run(debug=True)