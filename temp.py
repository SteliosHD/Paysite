import datetime
def get_wage(start_time,end_time):
    WPH = 3.91
    WPM = 3.91/60
    WEIGHT = 1
    normalHours = 0
    normalMinutes = 0
    afterHours = 0
    afterMinutes = 0
    import pdb; pdb.set_trace()
    if end_time.hour >= 22:
        date = datetime.date(1, 1, 1)
        start = datetime.datetime.combine(date, start_time)
        end = datetime.datetime.combine(date, datetime.time(22, 0, 0))
        normalHours += (end - start).seconds//3600
        normalMinutes += ((end - start).seconds % 3600)//60
        start = datetime.datetime.combine(date, datetime.time(22, 0, 0))
        end = datetime.datetime.combine(date, end_time)
        afterHours += (end - start).seconds//3600
        afterMinutes += ((end - start).seconds % 3600)//60
    if end_time.hour < 5:
        date1 = datetime.date(1, 1, 1)
        date2 = datetime.date(1, 1, 2)  # date has changed after 12 oclock
        start = datetime.datetime.combine(date1, start_time)
        end = datetime.datetime.combine(date1, datetime.time(22, 0, 0))
        normalHours += (end - start).seconds//3600
        normalMinutes += ((end - start).seconds % 3600)//60
        start = datetime.datetime.combine(date1, datetime.time(22, 0, 0))
        end = datetime.datetime.combine(date2, end_time)
        afterHours += (end - start).seconds//3600
        afterMinutes += ((end - start).seconds % 3600)//60
    if date.weekday() == 7:
        WEIGHT += 0.75
    wage = ((normalHours*WPH + normalMinutes*WPM)*WEIGHT) + \
        ((afterHours*WPH + afterMinutes*WPM)*(WEIGHT+0.25))
    return wage

if __name__ == "__main__":
    start_time = datetime.time(20, 34, 0)
    end_time = datetime.time(23, 34, 0)
    print(get_wage(start_time,end_time))
