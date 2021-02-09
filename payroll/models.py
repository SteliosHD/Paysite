from django.db import models
from django.shortcuts import reverse
# Create your models here.
import datetime # for dates and times   
import calendar # for making the day in string format

class Shift(models.Model):
    # fields
    identity = models.AutoField(("ID"),primary_key=True,auto_created=True)
    date =  models.DateField(("Date of Shift"), auto_now=False, auto_now_add=False)
    start_time = models.TimeField(("Start Time"), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(("End Time"), auto_now=False, auto_now_add=False)
    tip = models.DecimalField(("tip"), max_digits=4,
                              decimal_places=2)

    def __str__(self):
        return "#"+str(self.identity)+"-"+str(self.date)
    
    def get_duration(self):
        # get the duration of the given shift for display purposes
        date = datetime.date(1,1,1)
        start = datetime.datetime.combine(date,self.start_time)
        end = datetime.datetime.combine(date, self.end_time)
        durationS = (end - start).seconds
        durationHour = durationS//3600
        durationMinutes = (durationS%3600)//60

        return (durationHour,durationMinutes)
    
    def get_day(self):
        # get the day in day format using calendar 
        return calendar.day_name[self.date.weekday()]  

    def get_wage(self):
        # calculate the wage based on my needs
        WPH = 3.91
        WPM = 3.91/60
        WEIGHT = 1
        normalHours = 0
        normalMinutes = 0
        afterHours = 0
        afterMinutes = 0
        if self.end_time.hour>=22:
            date = datetime.date(1, 1, 1)
            start = datetime.datetime.combine(date, self.start_time)
            end = datetime.datetime.combine(date,datetime.time(22,0,0))
            normalHours += (end - start).seconds//3600
            normalMinutes += ((end - start).seconds % 3600)//60
            start = datetime.datetime.combine(date, datetime.time(22, 0, 0))
            end = datetime.datetime.combine(date, self.end_time)
            afterHours += (end - start).seconds//3600
            afterMinutes += ((end - start).seconds % 3600)//60
        elif self.end_time.hour<5:
            date1 = datetime.date(1, 1, 1)
            date2 = datetime.date(1, 1, 2) # date has changed after 12 oclock
            start = datetime.datetime.combine(date1, self.start_time)
            end = datetime.datetime.combine(date1, datetime.time(22, 0, 0))
            normalHours += (end - start).seconds//3600
            normalMinutes += ((end - start).seconds % 3600)//60
            start = datetime.datetime.combine(date1, datetime.time(22, 0, 0))
            end = datetime.datetime.combine(date2,self.end_time)
            afterHours += (end - start).seconds//3600
            afterMinutes += ((end - start).seconds % 3600)//60
        else:
            date = datetime.date(1, 1, 1)
            start = datetime.datetime.combine(date, self.start_time)
            end = datetime.datetime.combine(date, self.end_time)
            normalHours += (end - start).seconds//3600
            normalMinutes += ((end - start).seconds % 3600)//60
        if self.date.weekday()==6:
            WEIGHT += 0.75
        wage = ((normalHours*WPH + normalMinutes*WPM)*WEIGHT) + ((afterHours*WPH + afterMinutes*WPM)*(WEIGHT+0.25))
        return wage
    
    def get_absolute_url(self):
        # get the absolute url, needed for making the detail view of the shifts
        return reverse("payroll:shift", kwargs={"pk": self.pk})
    

