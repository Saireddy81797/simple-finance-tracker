from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = 'expenses.csv'

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Category', 'Amount'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount])

    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    expenses = []
    total = 0
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
            total += float(row['Amount'])

    return render_template('summary.html', expenses=expenses, total=total)

if __name__ == '__main__':
    app.run(debug=True)
