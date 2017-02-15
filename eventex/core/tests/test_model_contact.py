from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModel(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Henrique Bastos',
            slug='henrique-bastos',
            photo='http://hbn.link/hb-pic'
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                                         value='henrique@bastos.net')

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE,
                                         value='62-99372-0467')

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind shold be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL,
                          value='henrique@bastos.net')
        self.assertEqual('henrique@bastos.net', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Danilo Rodrigues',
            slug='danilo-rodrigues',
            photo='https://goo.gl/gmfyPZ'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='danilo.roddrigues@outlook.com')
        s.contact_set.create(kind=Contact.PHONE, value='62-99372-0467')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['danilo.roddrigues@outlook.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['62-99372-0467']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
