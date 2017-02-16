from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionCreate(CreateView):
    model = Subscription
    form_class = SubscriptionForm

    def form_valid(self, form):
        """Form is valid"""
        response = super().form_valid(form)
        self.send_email()
        return response

    def send_email(self):
        # Send subscription email
        template_name = 'subscriptions/subscription_email.txt'
        context = {'subscription': self.object}
        subject = 'Confirmaçao do inscriçao'
        from_ = settings.DEFAULT_FROM_EMAIL
        to = self.object.email

        body = render_to_string(template_name, context)
        return mail.send_mail(subject, body, from_, [from_, to])


new = SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)
