from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import calendar
from calendar import HTMLCalendar
from events.models import Event, Venue, MyClubUser
from django.http import HttpResponseRedirect, FileResponse
from events.form import VenueForm
from django.template.response import TemplateResponse
import csv
from django.http import FileResponse 
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class Register(CreateView): #createview класс делающий пустую форму редактирования
    template_name = 'registration/register.html' # шаблон формы редактрирования 
    form_class = UserCreationForm # форма для использования с CreateView. Мы используем UserCreationForm для создания формы
    success_url = reverse_lazy('register-success') # сюда пересылаем после успешного обработки формы 
                                                    # reverse_lazy для возврата url во время выполнения
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def list_subscribers(request):
    p = Paginator(MyClubUser.objects.all(), 3)
    page = request.GET.get('page')
    subscribers = p.get_page(page)
    return render(request,
                  'events/subscribers.html',
                  {'subscribers': subscribers})
def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
            # assert False
    return render(request,
                  'events/add_venue.html',
                  {'form': form, 'submitted': submitted})

def all_events(request):
    event_list = Event.objects.all()
    return render(request, 
                  'events/event_list.html',
                  {'event_list': event_list})


def index(request, year=date.today().year, month=date.today().month):
    # usr = request.user
    # ses = request.session
    # path = request.path_info
    # headers = request.headers
    # t = date.today()
    # month = date.strftime(t, '%b') # %b месяц в 3 символа упаковывает \ strftime методы строокового отображения времени 😀
    # year = t.year
    announcements = [
        {
            'date': '6-10-2020',
            'announcement': 'club registration'
        }
    ]
    year = int(year)
    month = int(month)
    if year < 2000 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    title = f'{month_name} {year}'
    cal = HTMLCalendar().formatmonth(year, month)
    # для времени

    # return HttpResponse('<h1>%s</h1><p>%s</p>' % (title, cal))
    return TemplateResponse(request, 'events/calBase.html', {'title': title, 'cal': cal, 'announcements': announcements})