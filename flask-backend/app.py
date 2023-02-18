from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from indicator_data import get_indicator_data, get_indicator_info
from news import get_news

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
    return jsonify(df)

@app.route('/getIndicatorInfo', methods=['GET'])
def get_data_ind():
    path = request.args
    name = path.get('name')
    ticker = path.get('ticker') + '.NS'
    interval = path.get('interval')
    period = path.get('period')
    indicator = path.get('indicator')
    print(name, ticker, interval, period, indicator)
    df = get_indicator_info(name, ticker, interval, period, indicator)
    return jsonify(df)

@app.route('/getCompanyNews', methods=['GET'])
def get_company_news():
    path = request.args
    name = path.get('name')
    df = get_news(name)
    return jsonify(df)

if __name__ == '__main__':
    app.run(debug=True)