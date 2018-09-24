import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils import getNextPrayer, convert2DateTime, convert2UTC
import os
import time


link = 'http://www.habous.gov.ma/horaire%20de%20priere%20fr/defaultmois.php?ville={}&mois={}'
city_code = '69' # Rabat
month_code = '09' # September


def buildDayPrayerDict(aList):
    _prayerDict = {}
    _prayerDict['day'] = aList[0].text.strip()
    prayers_name = ['fajr', 'chourouq', 'dhuhr', 'asr', 'maghrib', 'ishae']
    prayers_time = list(map(lambda x: x.text.strip(), aList[1:]))
    prayers_time = list(map(convert2UTC, prayers_time))
    time_left, prayer_idx = getNextPrayer(prayers_time)
    _prayers = []
    for i in range(len(prayers_name)):
        _d = {
            'name': prayers_name[i],
            'time': prayers_time[i],
            'next_prayer': True if i == prayer_idx else False,
            'time_left': time_left if i == prayer_idx else None
            }
        _prayers.append(_d)
    _prayerDict['prayers'] = _prayers
    return _prayerDict


def parsePrayerTimes(content):
    soup = BeautifulSoup(content, 'html.parser')
    prayer_table = soup.find('table', id='horaire')
    td_list = prayer_table.findAll('td')[9:]
    nb_days = int(len(td_list)/7)
    rows = []
    for i in range(nb_days):
        row = td_list[7*i: 7*(i+1)]
        rows.append(row)
    return rows


def getPrayers():
    prayers = []
    status = 'success'
    resp = requests.get(link.format(city_code, month_code))
    if resp.status_code == 200:
        rows = parsePrayerTimes(resp.content)
        for row in rows:
            prayerDict = buildDayPrayerDict(row)
            prayers.append(prayerDict)
    else:
        status = 'error: unable to fetch data'

    return (status, prayers)




if __name__ == '__main__':
    today = datetime.today().date().day
    status, prayers = getPrayers()
    if status == 'success':
        print(prayers[today-1])
    else:
        print(status)
