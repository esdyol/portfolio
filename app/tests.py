from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Freddy Ewinsou")

    def test_valid_contact_form_creates_message(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Alice",
                "email": "alice@example.com",
                "subject": "Collaboration",
                "message": "Bonjour Freddy",
            },
        )

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_contact_form_returns_errors(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "",
                "email": "invalid-email",
                "subject": "",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Le formulaire contient des erreurs.", status_code=400)
        self.assertEqual(ContactMessage.objects.count(), 0)
