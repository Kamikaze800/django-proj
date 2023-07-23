import csv
from django.contrib import admin
from django.contrib.auth.models import User, Group
# Register your models here.
from .models import Venue, MyClubUser, Event, Subscriber
# admin.site.register(Venue)
# admin.site.register(MyClubUser)
# admin.site.register(Event)
from django.contrib.admin import AdminSite
from events.form import VenueForm
from django.http import HttpResponse
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.admin import UserAdmin

class MyClubUserInline(admin.StackedInline):
    model = MyClubUser
    can_delete = False
    verbose_name = "Address and Phone"
    verbose_name_plural = "Additional Info"

class MyClubUserAdmin(UserAdmin):
    inlines = (MyClubUserInline,)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'member_level')
    list_filter = ('member_level',)

admin.site.unregister(User)
admin.site.register(User, MyClubUserAdmin)

class EventAdminForm(forms.ModelForm):
    name = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Event
        fields = '__all__'


def venue_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venue_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['name', 'time', 'venue'])
    for record in queryset:
        rec_list = []
        rec_list.append(record.name)
        rec_list.append(record.time.strftime("%m/%d/%Y, %H:%M"))
        rec_list.append(record.venue.name)
        writer.writerow(rec_list)
    return response
venue_csv.short_description = 'Export Selected Venues ro CSV'

def set_manager(modeladmin, request, queryset):
    queryset.update(manager=request.user)
set_manager.short_description = 'Manage selected events'

class AttendeeInline(admin.TabularInline):
    model = Event.users.through
    verbose_name = 'User'
    verbose_name_plural = 'Users'

class EventInline(admin.TabularInline):
# class EventInline(admin.StackedInline):
    model = Event
    fields = ('name', 'time')
    extra = 1

class EventsAdmin(AdminSite):
    site_header = 'Sosi event individ'
    site_title = 'Event admin'
    index_title = 'Events Home Sosi'

admin_site = EventsAdmin(name='eventsadmin')
admin_site.register(User)
admin_site.register(Group)

@admin.register(Venue, site=admin_site)
class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    list_display = ['name', 'email']
    ordering = ['name']
    search_fields = ['name']
    list_editable = ['email']
    save_as = True
    inlines = [
        EventInline,
        # AttendeeInline,
    ]
    list_display_links = ['name']
    # list_display_links = None
    def get_list_display(self, request):
        return('name', 'web', 'email')



@admin.register(Event, site=admin_site)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    actions = [set_manager, venue_csv]
    # fields = [('name', 'venue'), 'manager']
    list_display = ['name', 'manager', 'time']
    list_filter = ['time', 'venue']
    odering = ('-time',)
    list_display_links = ['name']
    # list_editable = list_display
    fieldsets = [
        ['Required Information',{
            'description': 'These fields are reauired for each event',
            'fields': (('name', 'venue'), 'time')
            }],
        ('Optional Info', {
            'classes': ('collapse', ),
            'description': 'These fields aren"t reauired for each event',
            'fields': ('manager',)
        }),
    ]
    inlines = [
        # EventInline,
        AttendeeInline,
    ]

@admin.register(MyClubUser, site=admin_site)
class MyClubUserAdmin(admin.ModelAdmin):
    list_display = ['firstName', 'secondName', 'age', 'email']
    list_display_links = None
    list_editable = list_display
