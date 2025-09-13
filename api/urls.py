from django.urls import path,include
from .views.api_views import CategoryViewSet, ProductViewSet, ClientViewSet, FAQViewSet, SubCategoryViewSet, TestimonialViewSet, TagViewSet, BlogPostViewSet, careers_apply, contact_submit, quote_submit,get_products,get_subcategories
from rest_framework.routers import DefaultRouter
from .views.html_views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'blogs', BlogPostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'subcategories', SubCategoryViewSet)  # Assuming you want to use the same viewset for subcategories

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('services/private_label_manufacturing/', service, name='services'),
    path('services/third_party_manufacturing/', manafacturing, name='manafacturing'),
    path('blog/',blogs,name='blogs'),
    path('facecare/',facecare,name='facecare'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('careers/', careers, name='careers'),
    path('careers/<int:job_id>/', career_detail, name='careers_detail'),
    path('services/formulation_and_customization/', innovation, name='innovation'),
    path('services/research_and_development/',research,name='research'),
    path('api/contact_submit/', contact_submit, name='contact_submit'),
    path('api/quote_submit/', quote_submit, name='quote_submit'),
    path('api/careers_apply/', careers_apply, name='careers_apply'),
    path('haircare/', haircare, name='haircare'),
    path('bodycare/', bodycare, name='bodycare'),
    path('mens_grooming/', mens_grooming, name='mens_grooming'),
    path('blog/<int:id>/', blog_detail, name='blog_detail'),
    path('medicated/', medicated, name='medicated'),
    path('mothercare/',mothercare,name='mothercare'),
    path('intimatecare/', intimatecare, name='intimatecare'),
    path('veterinary/',veterinary, name='veterinary'),
    path("get-subcategories/<int:category_id>/", get_subcategories, name="get_subcategories"),
    path("get-products/", get_products, name="get_products"),

    # path('test_slider/',test_slider, name='test_slider'),
    
]