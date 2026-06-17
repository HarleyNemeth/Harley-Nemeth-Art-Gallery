from django.db import models

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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class AboutSection(models.Model):
    heading = models.CharField(max_length=100, default="About Me")
    paragraph_1 = models.TextField()
    paragraph_2 = models.TextField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.heading