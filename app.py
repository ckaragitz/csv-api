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
    csv_input = csv.reader(stream)
    #print("file contents: ", file_contents)
    #print(type(file_contents))
    print(csv_input)
    for row in csv_input:
        print(row)

    stream.seek(0)
    result = stream.read()

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

if __name__ == '__main__':
    app.run(debug=True)