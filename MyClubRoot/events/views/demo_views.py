from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event, Venue, MyClubUser
from django.http import HttpResponseRedirect, FileResponse
from django.template.response import TemplateResponse
import csv
from django.http import FileResponse 
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.core import serializers
from datetime import datetime
from django.template import RequestContext, Template
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView

class MonthArchiveViewDemo(MonthArchiveView):
    queryset = Event.events.all()
    date_field = 'time'
    context_object_name = 'event_list'
    allow_future = True
    month_format = '%m'

class DeleteViewDemo(DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('show-events')

class UpdateViewDemo(UpdateView):
    model = Event
    fields = ['name', 'venue']
    template_name_suffix = '_update_form' #изменения суффикса поиска(по стандарту dj ищет <model>_form)
    success_url = reverse_lazy('show-events')

class CreateViewDemo(CreateView):
    model = Event
    fields = ['name', 'time', 'venue']
    success_url = reverse_lazy('show-events')

class ListViewDemo(ListView):
    model = Event
    context_object_name = 'all_events'

class DetailViewDemo(DetailView):
    model = Event
    context_object_name = 'event'

class TemplateViewDemo(TemplateView):

    template_name = 'events/cbv_demo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Testing The TemplateView CBV'
        return context

def context_demo(request):
    # template = Template('{{ user }}<br>{{ perms }}<br>{{ request }}<br>{{ messages }}')
    template = Template('{{ LANGUAGE_CODE }}<br>{{ LANGUAGE_BIDI }}')
    con = RequestContext(request)
    return HttpResponse(template.render(con))

def template_demo(request):
    empty_list = []
    color_list = ['red', 'green', 'blue', 'yellow']
    somevar = 5
    anothervar = 21
    today = datetime.now()
    past = datetime(1985, 11, 5)
    future = datetime(2035, 11, 5)
    best_bands = [
        {'name': 'The Angels', 'country': 'Australia'},
        {'name': 'Rammstein', 'country': 'Germany'},
        {'name': 'Nirvana', 'country': 'USA'},
        {'name': 'AC/DC', 'country': 'Australia'},
        {'name': 'The Offspring', 'country': 'USA'},
        {'name': 'Irom Maiden', 'country': 'UK'},
    ]
    aussie_bands = ['Australia', ['The Angels', 'AC/DC', 'The Living End']]
    venues_js = serializers.serialize('json', Venue.venues.all())
    return render(request,
                  'events/template_demo.html',
                  {'somevar': somevar,
                  'anothervar': anothervar,
                  'empty_list': empty_list,
                  'color_list': color_list,
                  'best_bands': best_bands,
                  'today': today,
                  'past': past, 
                  'future': future,
                  'aussie_bands': aussie_bands,
                  'venues': venues_js})

def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica-Oblique', 14)
    lines = [
        'I will not expose ignorance of the faculty.',
        'I will not conduct my own fire drills,', 
        'I will not prescribe.',
    ]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='bart.pdf')


def gen_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="bart.txt"'
    lines = [
        'I will not expose the ignorance of the faculty.\n',
        'I will not conduct my own fire drills.\n',
        'I will not prescribe medication.\n',
    ]
    response.writelines(lines)
    return response

def gen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)
    venues = Venue.venues.all()
    writer.writerow(['Venue Name', 'Web', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.web, venue.email])
    return response

def get_file(request):
    return FileResponse(open('downloads/sos.pdf', 'rb'))