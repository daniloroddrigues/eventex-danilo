from django.contrib import messages
from django.core import mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':

        form = SubscriptionForm(request.POST)
        """
        Valida post, caso seja valido retorna um http response redirect 302,
        se nao retorna um http response 200
        """
        if form.is_valid():

            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)

            mail.send_mail('Confirmaçao do inscriçao',
                           body,
                           'contato@eventex.com.br',
                           ['contato@eventex.com.br', form.cleaned_data['email']])

            messages.success(request, 'Inscriçao realizada com sucesso!')

            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
