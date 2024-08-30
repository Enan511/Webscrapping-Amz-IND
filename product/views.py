# views.py
import re
import requests as req
from bs4 import BeautifulSoup
from django.shortcuts import render
from .forms import AmazonProductForm


def fetch_amazon_product_details(url):
    pattern = r"(https:\/\/www\.amazon\.[a-z\.]+\/(?:[^\/]+\/dp\/|dp\/)[^\/]+\/)"
    cleanLink = re.search(pattern, url)

    if not cleanLink:
        return None, None, None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }

    product_response = req.get(url, headers=headers)
    soup = BeautifulSoup(product_response.content, 'html.parser')

    try:
        product_title = soup.find(id='productTitle').get_text().strip()
        product_price = soup.find(class_='a-price-whole').get_text().strip()
        product_image = soup.find(id="landingImage")['src']
    except AttributeError:
        return None, None, None

    return product_title, product_price, product_image


def amazon_product_view(request):
    if request.method == 'POST':
        form = AmazonProductForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            product_title, product_price, product_image = fetch_amazon_product_details(url)

            context = {
                'form': form,
                'product_title': product_title,
                'product_price': product_price,
                'product_image': product_image,
            }

            return render(request, 'product_details.html', context)
    else:
        form = AmazonProductForm()

    return render(request, 'product_details.html', {'form': form})
