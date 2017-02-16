from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionCreate(TemplateResponseMixin, View):
    template_name = 'subscriptions/subscription_form.html'
    form_class = SubscriptionForm

    def get(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, *args, **kwargs):
        """Valida post, caso seja valido retorna um http response redirect 302,
        se nao retorna um http response 200"""
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)
        return self.form_valid(form)

    def form_invalid(self, form):
        """Form is invalid"""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """Form is valid"""
        subscription = form.save()

        _send_mail('subscriptions/subscription_email.txt',
                   {'subscription': subscription},
                   'Confirmaçao do inscriçao',
                   settings.DEFAULT_FROM_EMAIL,
                   subscription.email)

        return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))

    def get_form(self):
        if self.request.method == 'POST':
            return self.form_class(self.request.POST)
        return self.form_class()

    def get_context_data(self, **kwargs):
        context = dict(kwargs)
        context.setdefault('form', self.get_form())
        return context


new = SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
