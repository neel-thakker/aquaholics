from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from indicator_data import get_indicator_data

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Test"

@app.route('/data', methods=['POST'])
def get_data():
    path = request.get_json(force=True)
    name = path['name']
    interval = path['interval']
    period = path['period']
    print(name, interval, period)
    df = get_indicator_data(name, interval, period)
    analysis = get_analysis(df)
    print(df)
    return jsonify(df)

@app.route('/getCompanyInfo', methods=['GET'])
def get_data_m():
    path = request.args
    name = path.get('name')
    ticker = path.get('ticker') + '.NS'
    interval = path.get('interval')
    period = path.get('period')
    print(name, ticker, interval, period)
    df = get_indicator_data(name, ticker, interval, period)
    print(df)
    return jsonify(df)

if __name__ == '__main__':
    app.run(debug=True)