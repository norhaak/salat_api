from flask import Flask, render_template
from api import getPrayers
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.today().date()
    date = today.strftime('%d/%m/%Y')
    city = 'Rabat Salé'
    status, prayers = getPrayers()
    if status != 'success':
        print(status)
    prayers = prayers[today.day -1]
    return render_template('index.html', 
            city=city,
            date=date,
            prayers=prayers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)