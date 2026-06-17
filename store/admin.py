from django.contrib import admin
from .models import Category, Artwork, AboutSection

admin.site.register(Category)
admin.site.register(Artwork)
admin.site.register(AboutSection)