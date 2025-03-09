from django.urls import path,include
from .views.api_views import CategoryViewSet, ProductViewSet, ClientViewSet, FAQViewSet, TestimonialViewSet, TagViewSet, BlogPostViewSet
from rest_framework.routers import DefaultRouter
from .views.html_views import index, about
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'blogs', BlogPostViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
]