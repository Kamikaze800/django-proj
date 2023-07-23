from django.urls import path, re_path
from . import views
from .views import ListViewDemo, DetailViewDemo, CreateViewDemo, UpdateViewDemo, DeleteViewDemo
from django.views.generic.dates import ArchiveIndexView
from .models import Event
from .views import MonthArchiveViewDemo


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', MonthArchiveViewDemo.as_view(), name='event-montharchive'),
    path('eventarchive/',  ArchiveIndexView.as_view(model=Event, date_field='time')),
    path('event/delete/<int:pk>', DeleteViewDemo.as_view(), name='delete-event'),
    path('event/update/<int:pk>', UpdateViewDemo.as_view(), name='update-event'),
    path('events/event/add/', CreateViewDemo.as_view(), name='add-event'),
    path('events/event/<int:pk>', DetailViewDemo.as_view(), name='event-detail'),
    path('condemo/', views.context_demo),
    path('tdemo', views.template_demo, name='tdemo'),
    path('getsubs', views.list_subscribers),
    path('genpdf', views.gen_pdf),
    path('gentext', views.gen_text),
    path('gencsv', views.gen_csv),
    path('pdf', views.get_file),
    path('add_venue', views.add_venue, name='add-venue'),
    path('events/', ListViewDemo.as_view() , name='show-events'),
    # path('<int:year>/<str:month>/', views.index, name='index'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
]