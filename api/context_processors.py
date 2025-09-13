from unicodedata import category
from api.models import WebsiteImages, Category, SubCategory, Product
from django.core.exceptions import ObjectDoesNotExist


def website_images(request):
    try:
        latest_version = WebsiteImages.objects.latest('created_at')
        categories = Category.objects.all()
        return {'website_images': latest_version, 'categories': categories}
    except ObjectDoesNotExist:
        return {'website_images': None}