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

    def test_store_groups_artwork_by_availability(self):
        sold_out = Artwork.objects.create(
            title="Sold Painting",
            price="30.00",
            category=self.category,
            available=True,
            stock=0,
        )
        not_offered = Artwork.objects.create(
            title="Unavailable Painting",
            price="35.00",
            category=self.category,
            available=False,
            stock=2,
        )

        response = self.client.get(reverse("store"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [section["heading"] for section in response.context["artwork_sections"]],
            ["Available Artwork", "Sold Out", "Not Currently Offered"],
        )
        content = response.content.decode()
        self.assertLess(content.index("Ikigai"), content.index("Sold Painting"))
        self.assertLess(content.index("Sold Painting"), content.index("Unavailable Painting"))
        self.assertContains(response, "Sold Out")
        self.assertContains(response, "Not Currently Available")
        self.assertContains(response, "Sold Painting")
        self.assertContains(response, "Unavailable Painting")
        self.assertNotContains(response, "Available Artwork")
        self.assertNotContains(response, "Not Currently Offered")
        self.assertContains(response, f'data-artwork-id="{self.artwork.id}"')
        self.assertNotContains(
            response,
            f'data-artwork-id="{sold_out.id}"',
        )
        self.assertNotContains(
            response,
            f'data-artwork-id="{not_offered.id}"',
        )

    def test_add_to_cart_rejects_sold_out_artwork(self):
        self.artwork.stock = 0
        self.artwork.save()

        response = self.client.get(
            reverse("add_to_cart", args=[self.artwork.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertNotIn(str(self.artwork.id), self.client.session.get("cart", {}))

    def test_add_to_cart_allows_available_artwork(self):
        response = self.client.get(
            reverse("add_to_cart", args=[self.artwork.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(self.client.session["cart"][str(self.artwork.id)], 1)

    def test_add_to_cart_rejects_artwork_not_offered_for_sale(self):
        self.artwork.available = False
        self.artwork.save()

        response = self.client.get(
            reverse("add_to_cart", args=[self.artwork.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertNotIn(str(self.artwork.id), self.client.session.get("cart", {}))
