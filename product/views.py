from django.shortcuts import render, redirect
from .forms import UploadCSVForm
from .models import Product
from .scripts import scrape_products_from_csv


def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Saved the uploaded file temporarily
            with open('temp.csv', 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Scraped product details from the CSV
            scraped_data = scrape_products_from_csv('temp.csv')

            # Saved data to the database
            for data in scraped_data:
                Product.objects.create(
                    title=data['title'],
                    price=data['price'],
                    image_url=data['image_url']
                )
            return redirect('product_list')
    else:
        form = UploadCSVForm()
    context = {'form': form,'title':'Info Scrapper'}
    return render(request, 'upload_csv.html', context)


def product_list(request):
    products = Product.objects.all()
    context = {'products': products, 'title': 'Product List'}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product, 'title': 'Product Detail'}
    return render(request, 'product_details.html', {'product': product})
