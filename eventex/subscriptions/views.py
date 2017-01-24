from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    """Valida post, caso seja valido retorna um http response redirect 302, se nao retorna um http response 200"""
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    _send_mail('subscriptions/subscription_email.txt',
               form.cleaned_data,
               'Confirmaçao do inscriçao',
               settings.DEFAULT_FROM_EMAIL,
               form.cleaned_data['email'])

    messages.success(request, 'Inscriçao realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/')


def new(request):
    return render(request, 'subscriptions/subscription_form.html',
                  {'form': SubscriptionForm()})


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
