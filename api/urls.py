from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'testimonials', views.TestimonialViewSet)
router.register(r'blogs', views.BlogPostViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]