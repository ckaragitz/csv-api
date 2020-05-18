from flask import Flask, request, jsonify, make_response, send_file
import gunicorn
import os
import io
import csv
import psycopg2

app = Flask(__name__)

@app.route('/leads/<job>', methods=["POST"])
def post_leads(job):

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    f = request.files['file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream)
    next(reader)

    print("...Loading data into Postgres...")
    for row in reader:
        row.append(str(job))
        print(row)
        cur.execute(
        'INSERT INTO "External_Lead" (id, first, last, phone, email, company, source, job_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
        (row)
        )

    conn.commit()
    print("...Complete...")

    stream.seek(0)
    result = stream.read()

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

@app.route('/leads/<job>', methods=["GET"])
def get_leads(job):

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    query = 'SELECT job_id FROM "External_Lead";'
    cur.execute("""SELECT job_id,first,last,phone,score FROM "External_Lead" WHERE job_id = '%s';""" % str(job))
    rows = cur.fetchall()
    print(rows)

    with open("lead_results.csv", 'w', encoding='utf-8') as out_file:
        w = csv.writer(rows, delimiter=' ')
        for row in rows:
            w.writerow(row)


    #construct file URL for download
    response = send_file('lead_results.csv', attachment_filename='lead_results.csv')
    return response
  
if __name__ == '__main__':
    app.run(debug=True)