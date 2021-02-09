from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ShiftForm

from .models import Shift

import datetime # for dates
from dateutil.parser import parse # for date parsing




class PostListView(ListView):
    form = ShiftForm()  # this needs form.py
    model = Shift
    template_name = 'payroll/index.html'
    context_object_name = 'Shift'   # change object name (default 'object')
    ordering = ['date'] # order the query set
    paginate_by = 10    # pagination
    queryset = model.objects.all() # get the query set

    def __init__(self,*args,**kwargs):
        # initialize some values to be access later
        super(PostListView,self).__init__(*args,**kwargs)
        self.date_min = self.get_date_to_show()[0]
        self.date_max = self.get_date_to_show()[1]
        self.queryset = self.queryset.filter(date__gte=self.date_min)
        self.queryset = self.queryset.filter(date__lte=self.date_max)

    
    @staticmethod
    def get_date_to_show():
        # get the default date
        curMonth = datetime.datetime.now().month
        curYear = datetime.datetime.now().year
        curDay = datetime.datetime.now().day
        if curDay>25:
            curDay = 25
        return (datetime.date(curYear, curMonth - 1, 25), datetime.date(curYear, curMonth , curDay))
    
    @staticmethod
    def is_valid_queryparam(param):
        # if we've passed any data in the search
        return param != '' and param is not None

    def set_dynamic_data(self,qs):
        # calculate dynamic data to display
        self.total_wage = 0
        self.total_tips = 0
        self.hours = 0
        self.minutes = 0
        for s in qs:
            self.total_wage += s.get_wage()
            self.total_tips += float(s.tip)
            self.hours += s.get_duration()[0]
            self.minutes += s.get_duration()[1]
        self.hours += self.minutes // 60
        self.minutes = self.minutes % 60
    
    def set_default_dates(self):
        # set default dates to show on the period info
        if self.date_min is None and self.date_max is None:
            self.date_min = self.get_date_to_show()[0]
            self.date_max = self.get_date_to_show()[1]
        elif self.date_min=='':
            self.date_min = self.queryset.first().date
        elif self.date_max=='':
            self.date_max = self.queryset.last().date
        


    def get_queryset(self):
        # filter the queryset appropriately and at the end odrder it again
        
        self.date_min = self.request.GET.get('shift_min_date')
        self.date_max = self.request.GET.get('shift_max_date')
        self.shiftMin = 'shift_min_date='+ str(self.date_min)
        self.shiftMax = 'shift_max_date=' + str(self.date_max)
        
        if (self.date_min and self.date_max) is None :
            self.dateURL = ''
        elif self.date_min is None:
            self.dateURL = '&'+self.shiftMax
        elif self.date_max is None:
            self.dateURL = '&'+self.shiftMin
        else:
            self.dateURL = '&'+self.shiftMin+'&'+self.shiftMax
            
        
        if self.date_min or self.date_max:
            qs = self.model.objects.all()
        else:
            qs = self.queryset
        if self.is_valid_queryparam(self.date_min):
            qs = qs.filter(date__gte=self.date_min)
            self.date_min = parse(self.date_min).date()
        if self.is_valid_queryparam(self.date_max):
            qs = qs.filter(date__lte=self.date_max)
            self.date_max = parse(self.date_max).date()
        self.set_dynamic_data(qs)
        qs = qs.order_by('date')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context['total_wage']= self.total_wage
        context['total_tips']= self.total_tips
        context['total_duration']= (self.hours,self.minutes)
        self.set_default_dates()
        context['dateURL'] = self.dateURL
        context['title'] = 'payroll'

        # get_copy = self.request.GET.copy()
        # if get_copy.get('page'):
        #     get_copy.pop('page')
        # context['get_copy'] = get_copy
        return context

    def post(self, request, *args, **kwargs):
        form = ShiftForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')


class PostDetailView(DetailView):
    model = Shift
    template_name = "payroll/shift.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'shift'
        return context


class PostUpdateView(UpdateView):
    model = Shift
    template_name = "payroll/shift_update.html"
    fields = ['date','start_time','end_time','tip']
    form = ShiftForm
    

    def get_context_data(self, **kwargs):
        # time passed wasn't a string so the form had no data
        # initialiazed it fix it 
        self.form = self.form(instance=self.object, initial={
            "start_time": self.object.start_time.strftime("%H:%M"),
            "end_time": self.object.end_time.strftime("%H:%M"),

            })
        context = super().get_context_data(**kwargs)
        context['title'] = 'shift'
        context['form'] = self.form
        return context
    



class PostDeleteView(DeleteView):
    model = Shift
    template_name = "payroll/shift_confirm_delete.html"
    success_url = "/"

# # Create your views here.
# # view with function
# def index(request):
#     form = ShiftForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect('/')

#     shift = Shift.objects.all()

#     def total_duarion():
#         hours = 0
#         minutes = 0
#         for s in shift:
#             hours += s.get_duration()[0]
#             minutes += s.get_duration()[1]
#         hours += minutes // 60
#         minutes = minutes % 60
#         return (hours,minutes)


#     total_wage = 0
#     total_tips = 0
#     for s in shift:
#         total_wage += s.get_wage()
#         total_tips += float(s.tip)
#     context = {
#         'form': form ,
#         'Shift': shift ,
#         'total_wage':total_wage,
#         'total_tips':total_tips,
#         'total_duration':total_duarion()
#     }
#     return render(request,"payroll/index.html",context)
