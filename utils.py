import datetime
from datetime import timedelta

prayers_time = ['05:48', '07:14', '13:24', '16:46', '19:25', '20:40']


def formatTimeDelta(time_left):
    time_left_ = (datetime.datetime.min + time_left).time()
    time_left_str = time_left_.strftime('%H:%M')
    return time_left_str



def convert2DateTime(time_str):
    current_date = datetime.datetime.now().date()
    time_ = datetime.datetime.strptime(time_str, '%H:%M').time()
    datetime_ = datetime.datetime.combine(current_date, time_)
    return datetime_

def convert2UTC(time_str):
    time_ = convert2DateTime(time_str)
    time_utc = time_ - timedelta(hours=1)
    time_str = time_utc.strftime('%H:%M')
    return time_str

def getNextPrayer(prayers_time):
    prayer_idx = None
    time_left = None

    current_datetime = datetime.datetime.now()
    for prayer_time in prayers_time:
        # convert prayer_time into datetime.datetime.time object
        prayer_datetime = convert2DateTime(prayer_time)
        if prayer_datetime > current_datetime:
            time_left = formatTimeDelta(prayer_datetime - current_datetime)
            prayer_idx = prayers_time.index(prayer_time)
            break

    return (time_left, prayer_idx)

if __name__ == '__main__':
    time_left, prayer_idx = getNextPrayer(prayers_time)
    if prayer_idx != None:
        print(prayers_time[prayer_idx])
        print('time left: {}'.format(time_left))