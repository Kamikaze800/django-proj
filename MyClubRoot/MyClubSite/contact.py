from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection
from django.views.generic.edit import FormView


class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(required=False, label = 'Your Email')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea) # позволяет вводить много текста

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # cleaned_data нормализует данные и созранаяет их в словарь
            # assert False
            con = get_connection('django.core.mail.backends.console.EmailBackend')
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'), 
                ['siteowner@example.com'],
                connection=con
            )
            # по факту это готовая рассылка, токо надо изменить серверное приложение
            # и в settings добавить настройки почтового сервера
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
        
    return render(request,
                  'contact/contact.html',
                  {'form': form, 'submitted': submitted}
    )

class ContactUs(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/contact?submitted=True'

    def get(self,request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)
    
    def form_valid(self, form):
        cd = form.cleaned_data
        con = get_connection('django.core.mail.backends.console.EmailBackend')
        send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'), 
                ['siteowner@example.com'],
                connection=con
            )
        return super().form_valid(form)    