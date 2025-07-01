from api.models import WebsiteImages


def website_images(request):
    return {
        'all_cultures': WebsiteImages.objects.latest('created_at')
    }