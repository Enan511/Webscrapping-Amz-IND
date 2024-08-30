# views.py
from django.shortcuts import render
from .forms import AmazonURLForm
from .scripts import AmazonScraper  # Adjust the import based on where Scripts.py is located


def product_details_view(request):
    if request.method == 'GET':
        form = AmazonURLForm(request.GET)
        if form.is_valid():
            url = form.cleaned_data['url']
            scraper = AmazonScraper(url)
            product_details = scraper.scrape_product_details()

            context = {
                "form": form,
                "product_title": product_details['title'],
                "product_price": product_details['price'],
                "product_image_url": product_details['image_url'],
            }
            return render(request, 'product_details.html', context)
        else:
            context = {"form": form}
    else:
        form = AmazonURLForm()
        context = {"form": form}

    return render(request, 'product_details.html', context)
