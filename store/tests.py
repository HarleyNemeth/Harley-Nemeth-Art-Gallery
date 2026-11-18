from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.test import override_settings

from .models import Artwork, Category, AboutSection, CommissionOffering


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

    def test_homepage_links_to_commission_enquiry(self):
        response = self.client.get(reverse("index"))

        self.assertContains(
            response,
            f'{reverse("contact")}?enquiry_type=commission',
        )

    def test_contact_page_displays_active_commission_offerings(self):
        offering = CommissionOffering.objects.create(
            title="Portrait Commission",
            description="A custom portrait in the artist's style.",
        )
        CommissionOffering.objects.create(
            title="Hidden Offering",
            description="Not currently listed.",
            is_active=False,
        )

        response = self.client.get(
            reverse("contact"),
            {"enquiry_type": "commission", "commission_offering": offering.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portrait Commission")
        self.assertNotContains(response, "Hidden Offering")
        self.assertEqual(response.context["form"]["inquiry_type"].value(), "commission")
        self.assertEqual(
            response.context["form"]["commission_offering"].value(),
            str(offering.id),
        )

    def test_commission_offerings_are_manageable_in_admin(self):
        offering = CommissionOffering.objects.create(
            title="Portrait Commission",
            description="A custom portrait in the artist's style.",
        )
        admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.test",
            password="test-password",
        )
        self.client.force_login(admin_user)

        response = self.client.get(
            reverse("admin:store_commissionoffering_changelist")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, offering.title)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="website@example.test",
    )
    def test_contact_form_sends_general_and_commission_details(self):
        offering = CommissionOffering.objects.create(
            title="Portrait Commission",
            description="A custom portrait in the artist's style.",
        )

        response = self.client.post(
            reverse("contact"),
            {
                "name": "Alex",
                "email": "alex@example.test",
                "inquiry_type": "commission",
                "commission_offering": str(offering.id),
                "project_size": "A4",
                "budget": "To be discussed",
                "timeframe": "Spring",
                "message": "I would like to discuss a portrait.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["sent"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Commission enquiry", mail.outbox[0].subject)
        self.assertIn("Commission type: Portrait Commission", mail.outbox[0].body)
        self.assertIn("Preferred size or format: A4", mail.outbox[0].body)
        self.assertIn("Approximate budget: To be discussed", mail.outbox[0].body)
        self.assertIn("I would like to discuss a portrait.", mail.outbox[0].body)

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
