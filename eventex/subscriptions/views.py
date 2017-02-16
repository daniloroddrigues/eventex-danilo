from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import ModelFormMixin

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionCreate(TemplateResponseMixin, ModelFormMixin, View):
    template_name = 'subscriptions/subscription_form.html'
    form_class = SubscriptionForm

    def get(self, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data())

    def post(self, *args, **kwargs):
        """Valida post, caso seja valido retorna um http response redirect 302,
        se nao retorna um http response 200"""
        self.object = None
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)
        return self.form_valid(form)

    def form_valid(self, form):
        """Form is valid"""
        self.object = form.save()

        _send_mail('subscriptions/subscription_email.txt',
                   {'subscription': self.object},
                   'Confirmaçao do inscriçao',
                   settings.DEFAULT_FROM_EMAIL,
                   self.object.email)

        return HttpResponseRedirect(self.get_success_url())


new = SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
