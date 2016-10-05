import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, redirect, abort

from calendar import Calendar
from datetime import date

import FTPCrawler

app = Flask(__name__)


@app.route('/')
@app.route('/<year>/<month>/<day>')
def index(year=None, month=None, day=None):
    cal = Calendar(0)

    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month
    if day is None:
        day = date.today().day

    cal_list = [cal.monthdatescalendar(year, i+1) for i in range(12)]

    return render_template('index.html', c_year=year, c_month=month, c_day=day, calendar=cal_list)
    # return render_template('cal.html', year=year, cal=cal_list)


@app.template_filter('date_month_format')
def _jinja2_filter_datetime(_date):
    return _date.strftime('%%Y%%m')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=FTPCrawler.backup_last_hour,
        trigger=IntervalTrigger(hours=1),
        id='backup_last_hour',
        name='Backup last one hour.',
        replace_existing=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # FTPCrawler.backup_last_hour()

    app.run(host='0.0.0.0', port=2024, debug=True)
