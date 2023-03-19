#!/usr/bin/env python

import alpha_vantage
from alpha_vantage.fundamentaldata import FundamentalData
from flask import Flask, render_template, request

app = Flask(__name__)

# Define the route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for the Cash Runway Calculator form
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the input from the form
    ticker = request.form['ticker']
    # Call the Cash Runway Calculator function
    try:
        fd = FundamentalData(key='T8R98OWSJ1F053EU', output_format='pandas')
        data, meta_data = fd.get_balance_sheet_quarterly(ticker)
        latest_quarter = data.iloc[0]
        cash_balance = int(latest_quarter['cashAndCashEquivalentsAtCarryingValue'])
        previous_quarter=data.iloc[1]
        old_cash=int(previous_quarter['cashAndCashEquivalentsAtCarryingValue'])
        rate=(old_cash-cash_balance)/3
        mcash=round(cash_balance/rate,2)
        qcash=mcash/3
        output = f"{ticker} has {mcash} Months or {qcash} Quarters of Cash left"
        error = None
    except Exception as e:
        error = f"An error occurred: {e}"
        output = None
    # Render the result template with the output and/or error
    return render_template('result.html', output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
