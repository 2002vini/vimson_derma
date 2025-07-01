from api.models import WebsiteImages
from django.core.exceptions import ObjectDoesNotExist


def website_images(request):
    try:
        latest_version = WebsiteImages.objects.latest('created_at')
        return {'website_images': latest_version}
    except ObjectDoesNotExist:
        return {'website_images': None}