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
    df = get_all_data(name, interval, period)
    return df.to_string()

if __name__ == '__main__':
    app.run(debug=True)