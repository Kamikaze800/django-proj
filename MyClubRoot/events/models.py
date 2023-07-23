from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

from django.contrib.auth.models import User

class VenueManager(models.Manager):
    def get_queryset(self):
        return super(VenueManager, self).get_queryset().filter(name='sosi')

class Venue(models.Model):
    name = models.TextField('Venom Name')
    web = models.URLField('web', blank=True)
    email = models.EmailField('email', blank=True)
    venues = models.Manager()
    local_venues = VenueManager()
    def __str__(self):
        return self.name
    
class MyClubUser(models.Model):
    firstName = models.CharField(verbose_name='firstName', max_length=200)
    secondName = models.CharField(verbose_name='secondName', blank=True, max_length=200)
    email = models.EmailField('email', blank=True)
    age = models.PositiveSmallIntegerField(default=0)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=100)
    volunteer = models.BooleanField(default=False)

    def __str__(self):
        # return f'{self.firstName} {self.secondName}'
        return ''
    
MEMBER_CHOICES = [
    ('A', 'Adult'),
    ('J', 'Junior'),
    ('C', 'Concession'),
]

class Subscriber(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    member_level = models.CharField(max_length=1, choices=MEMBER_CHOICES, default='A')
    

class EventManager(models.Manager):
    def event_type_count(self, event_type):
        return self.filter(name__icontains=event_type).count()
    

class Event(models.Model):
    name = models.TextField('name', null=True, blank=True)
    time = models.DateTimeField('time', default=timezone.now)
    venue = models.ForeignKey(Venue, blank=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(MyClubUser, blank=True)
    events = EventManager()
    def event_timing(self, date):
        if self.time > date:
            return 'Event is after this date'
        elif self.time == date:
            return 'Event is on the same day'
        else:
            return 'Event is before this day'
    
    def save(self, *args, **kwargs):
        self.manager = User.objects.get(username='admin')
        super(Event, self).save(*args, **kwargs)
        
    @property
    def name_slug(self):
        return self.name.lower().replace(' ', '-')
    
    def __str__(self):
        return f"{self.name} ({self.time})"
    