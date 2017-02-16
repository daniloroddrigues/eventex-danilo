from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseCreateView

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionCreate(TemplateResponseMixin, BaseCreateView):
    template_name = 'subscriptions/subscription_form.html'
    form_class = SubscriptionForm

    def form_valid(self, form):
        """Form is valid"""
        response = super().form_valid(form)

        _send_mail('subscriptions/subscription_email.txt',
                   {'subscription': self.object},
                   'Confirmaçao do inscriçao',
                   settings.DEFAULT_FROM_EMAIL,
                   self.object.email)

        return response


new = SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
