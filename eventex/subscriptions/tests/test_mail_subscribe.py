from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Danilo Rodrigues', cpf='12345678901',
                    email='danilo.roddrigues@outlook.com', phone='62-99372-0467')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmaçao do inscriçao'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'danilo.roddrigues@outlook.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Danilo Rodrigues',
            '12345678901',
            'danilo.roddrigues@outlook.com',
            '62-99372-0467',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
