
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = Flask(__name__)

LAUNCH_DATA = {
    'BTC': {'date': '2009-01-03', 'time': '18:15', 'location': 'London'},
    'ETH': {'date': '2015-07-30', 'time': '15:26', 'location': 'Zurich'},
    'DOGE': {'date': '2013-12-06', 'time': '12:00', 'location': 'San Francisco'},
}

CITY_COORDS = {
    'London': GeoPos('51.5074', '-0.1278'),
    'Zurich': GeoPos('47.3769', '8.5417'),
    'San Francisco': GeoPos('37.7749', '-122.4194')
}

def get_direction(chart):
    moon = chart.get(const.MOON)
    jupiter = chart.get(const.JUPITER)
    if moon.sign == 'SCORPIO' and jupiter.sign == 'TAURUS':
        return 'Long'
    elif moon.sign == 'VIRGO' and jupiter.sign == 'ARIES':
        return 'Short'
    return 'Neutral'

@app.route('/predict', methods=['GET'])
def predict():
    coin = request.args.get('coin', '').upper()
    data = LAUNCH_DATA.get(coin)
    if not data:
        return jsonify({'error': 'Coin launch data not found'}), 404

    now = datetime.utcnow()
    predictions = []
    for i in range(0, 60, 10):
        ts = now + timedelta(minutes=i)
        date_str = ts.strftime('%Y/%m/%d')
        time_str = ts.strftime('%H:%M')
        pos = CITY_COORDS.get(data['location'], CITY_COORDS['London'])
        chart = Chart(Datetime(date_str, time_str, '+00:00'), pos)
        direction = get_direction(chart)
        time_window = f"{ts.strftime('%H:%M')}–{(ts + timedelta(minutes=10)).strftime('%H:%M')}"
        moon = chart.get(const.MOON)
        jupiter = chart.get(const.JUPITER)
        predictions.append({
            'time': time_window,
            'planet1': f"{moon} ({moon.sign})",
            'planet2': f"{jupiter} ({jupiter.sign})",
            'direction': direction
        })

    return jsonify({'coin': coin, 'predictions': predictions})

if __name__ == '__main__':
    app.run(debug=True)
