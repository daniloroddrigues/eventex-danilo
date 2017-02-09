from django.conf import settings
from django.core import mail
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    return render(request, 'subscriptions/subscription_form.html',
                  {'form': SubscriptionForm()})


def create(request):
    """Valida post, caso seja valido retorna um http response redirect 302,
    se nao retorna um http response 200"""
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    subscription = form.save()

    _send_mail('subscriptions/subscription_email.txt',
               {'subscription': subscription},
               'Confirmaçao do inscriçao',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email)

    return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))


def detail(request, pk):
    """Test view detail"""
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription})


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
