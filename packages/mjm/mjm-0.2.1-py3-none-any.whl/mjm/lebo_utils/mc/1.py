import time
import datetime
def get_date(sd,ed):
    sdl = sd.split(',')
    edl = ed.split(',')
    start_date = datetime.date(int(sdl[0]), int(sdl[1]), int(sdl[2]))
    end_date = datetime.date(int(edl[0]), int(edl[1]), int(edl[2]))

    date_array = []
    current_date = start_date

    while current_date <= end_date:

        dt = current_date.strftime('%Y%m%d')
        date_array.append(dt)
        current_date += datetime.timedelta(days=1)
    return date_array