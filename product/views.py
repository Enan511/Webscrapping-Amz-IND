import threading
from django.shortcuts import render
from .forms import UploadCSVForm
from .models import Product
from .scripts import scrape_products_from_csv


def background_scrape_and_save(csv_file_path):
    # Scrape product details from the CSV
    scraped_data = scrape_products_from_csv(csv_file_path)

    # Save data to the database, using get_or_create to avoid duplicates
    for data in scraped_data:
        Product.objects.get_or_create(
            title=data['title'],
            defaults={
                'price': data['price'],
                'image_url': data['image_url'],
                'description': data['description'],
            }
        )


def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Save the uploaded file temporarily
            temp_csv_path = 'temp.csv'
            with open(temp_csv_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Start the web scraping in a separate thread
            scrape_thread = threading.Thread(target=background_scrape_and_save, args=(temp_csv_path,))
            scrape_thread.start()

            # Show the "Thanks for the upload" message immediately
            return render(request, 'upload_confirmation.html', {'title': 'Upload Confirmation'})
    else:
        form = UploadCSVForm()
    context = {'form': form, 'title': 'Info Scrapper'}
    return render(request, 'upload_csv.html', context)


def product_list(request):
    products = Product.objects.all()
    context = {'products': products, 'title': 'Product List'}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product, 'title': 'Product Detail'}
    return render(request, 'product_details.html', context)
