from django.test import TestCase
from django.urls import reverse

from .models import Artwork, Category, AboutSection


class StorePageTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Paintings"
        )

        self.artwork = Artwork.objects.create(
            title="Ikigai",
            description="A painting inspired by Japanese philosophy.",
            price="45.00",
            category=self.category,
            available=True,
            featured=True,
            stock=1
        )

        self.about = AboutSection.objects.create(
            heading="About Me",
            paragraph_1="I am an artist.",
            paragraph_2="I create meaningful artwork."
        )

    def test_homepage_loads_successfully(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)

    def test_homepage_displays_featured_artwork(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.context["featured"], self.artwork)

    def test_homepage_displays_about_section(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.context["about"], self.about)

    def test_store_page_loads_successfully(self):
        response = self.client.get(reverse("store"))

        self.assertEqual(response.status_code, 200)

    def test_store_page_displays_artwork(self):
        response = self.client.get(reverse("store"))

        self.assertIn(self.artwork, response.context["artworks"])
