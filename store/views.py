from django.shortcuts import render
from .models import Artwork, AboutSection

def index(request):
    featured = Artwork.objects.filter(featured=True).first()
    about = AboutSection.objects.first()
    return render(request, 'store/index.html', {'featured': featured, 'about': about})

def store(request):
    artworks = Artwork.objects.all()
    return render(request, 'store/store.html', {'artworks': artworks})

from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f'New enquiry from {name}',
                message=f'From: {name} ({email})\n\n{message}',
                from_email=None,
                recipient_list=['dracohcn@gmail.com'],
            )
            sent = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'store/contact.html', {'form': form, 'sent': sent})
def cart(request):
    return render(request, 'store/cart.html')