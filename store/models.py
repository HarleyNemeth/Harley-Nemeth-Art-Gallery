from django.db import models
from django.core.validators import MinValueValidator
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Artwork(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='artworks')
    image_url = models.URLField(blank=True)
    hover_video_url = models.URLField(blank=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=50, blank=True)
    medium = models.CharField(max_length=100, blank=True)
    stock = models.PositiveIntegerField(default=1)
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first within each availability group.",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name="additional_images",
    )
    image_url = models.URLField()
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first.",
    )

    class Meta:
        ordering = ["display_order", "pk"]
        verbose_name = "Additional image"
        verbose_name_plural = "Additional images"

    def __str__(self):
        return f"{self.artwork.title} image {self.pk or 'new'}"

class AboutSection(models.Model):
    heading = models.CharField(max_length=100, default="About Me")
    paragraph_1 = models.TextField()
    paragraph_2 = models.TextField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.heading


class PastCommission(models.Model):
    title = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]
        verbose_name = "Past commission"
        verbose_name_plural = "Past commissions"

    def __str__(self):
        return self.title or "Past commission"

class Order(models.Model):
    #customer details
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    #delivery address
    shipping_address = models.CharField(max_length=200)
    shipping_address_2 = models.CharField(max_length=200, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    #order date
    created_at = models.DateTimeField(auto_now_add=True)
    #financial details
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    #payment status
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
    )
    #fulfillment status
    FULFILLMENT_STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    fulfillment_status = models.CharField(
        max_length=20,
        choices=FULFILLMENT_STATUS_CHOICES,
        default='processing',
    )

    #stripe references
    stripe_session_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"Order #{self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.PROTECT, related_name='order_items')
    artwork_title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.artwork_title} in Order #{self.order.pk}"