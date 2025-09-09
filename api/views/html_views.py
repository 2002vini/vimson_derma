from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages


from api.serializers import CategorySerializer, JobPositionSerializer, JobSerializer, SubCategorySerializer, TagSerializer,TestimonialSerializer,ProductSerializer,BlogPostSerializer
from ..models import BlogPost, Category, Job, JobPosition, SubCategory, Tag, Testimonial, Product, Category, FactFigure, \
    TrustedCompanies


def index(request):
    categories=Category.objects.filter(is_medicated=False)
    serialized_categories = CategorySerializer(categories, many=True,context={'request':request}).data 
    mid_index = len(serialized_categories) // 2
    categories_section_1 = serialized_categories[:mid_index]  # First half
    categories_section_2 = serialized_categories[mid_index:]  # Second half
    testimonials=Testimonial.objects.all().filter(is_featured=True).order_by('updated_at')
    serialized_testimonials = TestimonialSerializer(testimonials, many=True,context={'request':request}).data
    grouped_testimonials = [serialized_testimonials[i:i+3] for i in range(0, len(serialized_testimonials), 3)]  # Split into groups of 3
    context = {
        'category_section_1': categories_section_1,
        'category_section_2': categories_section_2,
        'grouped_testimonials': grouped_testimonials,
        'testimonials': serialized_testimonials,
        'facts_and_figures': FactFigure.objects.all()
    }
    return render(request, 'api/index.html', context)


def about(request):
    trusted_companies_ltr = TrustedCompanies.objects.filter(slider_direction="ltr")
    trusted_companies_rtl = TrustedCompanies.objects.filter(slider_direction="rtl")

    context = {
        'trusted_companies_ltr': trusted_companies_ltr,
        'trusted_companies_rtl': trusted_companies_rtl,
    }
    return render(request, 'api/about.html', context)


def service(request):
    categories = Category.objects.filter(is_medicated=False)
    serialized_categories=CategorySerializer(categories, many=True,context={'request':request}).data
    return render(request,'api/service.html',{'products':serialized_categories})


def manafacturing(request):
    categories = Category.objects.filter(is_medicated=False)
    serialized_categories=CategorySerializer(categories, many=True,context={'request':request}).data
    testimonials=Testimonial.objects.all()
    serialized_testimonials = TestimonialSerializer(testimonials, many=True,context={'request':request}).data

    trusted_companies_ltr = TrustedCompanies.objects.filter(slider_direction="ltr")
    trusted_companies_rtl = TrustedCompanies.objects.filter(slider_direction="rtl")

    context = {
        'products': serialized_categories,
        'testimonials':serialized_testimonials,
        'trusted_companies_ltr': trusted_companies_ltr,
        'trusted_companies_rtl': trusted_companies_rtl,
    }
    return render(request,'api/manafacturing.html', context)


def blogs(request):
    selected_tags=request.GET.get('tags')
    categories = Category.objects.all()
    blogs=BlogPost.objects.all()
    tags=Tag.objects.all()

    serialized_blog_post=BlogPostSerializer(blogs,many=True,context={'request':request}).data
    
    return render(request,'api/blogs.html',
                  {'blogs':serialized_blog_post})


def blog_detail(request, id):
    blog = BlogPost.objects.all().get(id=id)
    blog_serailized = BlogPostSerializer(blog, context={'request': request}).data
    return render(request, 'api/blog_detail.html', {'blog': blog_serailized})


def facecare(request):
    # Fetch all the products that need to be displayed
    products=Product.objects.all().filter(is_featured=False,category__type='FaceCare').order_by('updated_at')
    selected_tag = request.GET.get('filter')
    if selected_tag and selected_tag != 'All':
        products = products.filter(subcategory__type=selected_tag)  # Assuming 'tags' is a ManyToManyField in Product model
    #Fetch the page number from the request 
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    featured_products=Product.objects.all().filter(is_featured=True,category__type='FaceCare').order_by('updated_at')
    serialized_products = ProductSerializer(page_obj.object_list, many=True, context={'request': request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category__type='FaceCare'), many=True,context={'request':request}).data
    context = {
        'products':serialized_products,
        'page_obj':page_obj,
        'subcategory':serialized_sub_categories,
        'featured_products':serialized_featured_products
    }
    return render(request,'api/facecare.html',context)


def haircare(request):
    selected_subcategory = request.GET.get('filter')
    featured_products=Product.objects.all().filter(is_featured=True,category__type='HairCare').order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category__type='HairCare').order_by('updated_at')

    if selected_subcategory and selected_subcategory != 'All':
        products = products.filter(subcategory__type=selected_subcategory)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    serialized_products=ProductSerializer(page_obj.object_list,many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category__type='HairCare'), many=True,context={'request':request}).data
    context = {
        'products':serialized_products,
        'featured_products':serialized_featured_products,
        'subcategory':serialized_sub_categories,
        'page_obj': page_obj,
    }
    return render(request,'api/haircare.html', context)


def bodycare(request):
    selected_subcategory = request.GET.get('filter')
    page_number = request.GET.get('page', 1)
    featured_products=Product.objects.all().filter(is_featured=True,category__type='BodyCare').order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category__type='BodyCare').order_by('updated_at')
    if selected_subcategory and selected_subcategory != 'All':
        products = products.filter(subcategory__type=selected_subcategory)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    serialized_products=ProductSerializer(page_obj.object_list,many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category__type='BodyCare'), many=True,context={'request':request}).data
    context = {
        'products': serialized_products,
        'subcategory':serialized_sub_categories,
        'featured_products':serialized_featured_products,
        'page_obj': page_obj,
    }
    return render(request,'api/bodycare.html', context)


def mens_grooming(request):
    selected_subcategory = request.GET.get('filter')
    featured_products=Product.objects.all().filter(is_featured=True,category__type="Men's Grooming").order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category__type="Men's Grooming").order_by('updated_at')
    if selected_subcategory and selected_subcategory != 'All':
        products = products.filter(subcategory__type=selected_subcategory)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    serialized_products=ProductSerializer(page_obj.object_list,many=True,context={'request':request}).data
    serialized_categories=CategorySerializer(Category.objects.all(), many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category__type="Men's Grooming"), many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    context = {
        'products':serialized_products,
        'categories':serialized_categories,
        'subcategory':serialized_sub_categories,
        'featured_products':serialized_featured_products,
        'page_obj': page_obj,
    }
    return render(request,'api/mens_grooming.html', context)


def mothercare(request):
    selected_subcategory = request.GET.get('filter')
    featured_products=Product.objects.all().filter(is_featured=True,category__type='Baby & Mother Care').order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category__type='Baby & Mother Care').order_by('updated_at')
    if selected_subcategory and selected_subcategory != 'All':
        products = Product.objects.filter(is_featured=False, category__type='Baby & Mother Care', subcategory__type=selected_subcategory).order_by('updated_at')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    serialized_products=ProductSerializer(page_obj.object_list,many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category__type='Baby & Mother Care'), many=True,context={'request':request}).data
    context = {
        'products':serialized_products,
        'subcategory':serialized_sub_categories,
        'featured_products':serialized_featured_products,
        'page_obj': page_obj,
    }
    return render(request,'api/mothercare.html', context)


def product_detail(request,product_id):
    product=Product.objects.get(id=product_id)
    serialized_product=ProductSerializer(product,context={'request':request}).data
    return render(request,'api/product_detail.html',{'product':serialized_product})


def careers(request):
    Jobs=Job.objects.all()
    serialized_jobs=JobSerializer(Jobs,many=True,context={'request':request}).data
    positions=JobPosition.objects.all()
    serialized_positions=JobPositionSerializer(positions,many=True,context={'request':request}).data
    return render(request,'api/careers.html',{'jobs':serialized_jobs,'positions':serialized_positions})


def career_detail(request,job_id):
    job=Job.objects.get(id=job_id)
    remaining_top_jobs=Job.objects.exclude(id=job_id).order_by('-created_at')[:3]
    serialized_job=JobSerializer(job,context={'request':request}).data
    return render(request,'api/career_detail.html',{'job':serialized_job,'remaining_top_jobs':remaining_top_jobs})


def innovation(request):
    customized_products = Product.objects.filter(is_customized=True).order_by('updated_at')
    customized_product_serializers = ProductSerializer(customized_products, many=True, context={'request': request}).data
    return render(request,'api/formulation_and_customization.html',{'customized_products':customized_product_serializers})


def research(request):
    blogs=BlogPost.objects.all()
    serialized_blogs=BlogPostSerializer(blogs,many=True,context={'request':request}).data
    return render(request,'api/research.html',{'blogs':serialized_blogs})


def medicated(request):
    category_filter = request.GET.get('category')
    feautured_products = Product.objects.filter(is_featured=True, is_medicated=True).order_by('updated_at')
    serialized_featured_products = ProductSerializer(feautured_products, many=True, context={'request': request}).data
    if category_filter:
        products = Product.objects.filter(is_medicated=True, category__type=category_filter).order_by('updated_at')
    else:
        products = Product.objects.filter(is_medicated=True, category__type='FaceCare').order_by('updated_at')
        category_filter = 'FaceCare'  # Default category if none is selected
    serialized_products = ProductSerializer(products, many=True, context={'request': request}).data
    context = {
        'products':serialized_products,
        'selected_category':category_filter,
        'featured_products':serialized_featured_products
    }
    return render(request,'api/medicated.html', context)


def intimatecare(request):
    page_number = request.GET.get('page', 1)
    selected_subcategory = request.GET.get('filter')
    products = Product.objects.filter(category__type='Intimate Care').order_by('updated_at')

    if selected_subcategory and selected_subcategory != 'All':
        products = products.filter(subcategory__type=selected_subcategory)

    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list
    serialized_products = ProductSerializer(products, many=True, context={'request': request}).data
    featured_products = Product.objects.filter(is_featured=True, category__type='Intimate Care').order_by('updated_at')
    serialized_featured_products = ProductSerializer(featured_products, many=True, context={'request': request}).data
    serialized_sub_categories = SubCategorySerializer(SubCategory.objects.all().filter(category__type='Intimate Care'), many=True, context={'request':request}).data

    context = {
        'products': serialized_products,
        'featured_products': serialized_featured_products,
        'subcategory': serialized_sub_categories,
        'page_obj': page_obj,
    }
    return render(request, 'api/intimatecare.html', context)


def veterinary(request):
    selected_subcategory = request.GET.get('filter')
    page_number = request.GET.get('page', 1)
    featured_products=Product.objects.all().filter(is_featured=True,category__type='Veterinary').order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category__type='Veterinary').order_by('updated_at')
    if selected_subcategory and selected_subcategory != 'All':
        products = products.filter(subcategory__type=selected_subcategory)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list
    serialized_products = ProductSerializer(products,many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories = SubCategorySerializer(
        SubCategory.objects.all().filter(category__type='Veterinary'),
        many=True,
        context={'request':request}
    ).data

    context = {
        'products' : serialized_products,
        'featured_products' : serialized_featured_products,
        'subcategory' : serialized_sub_categories,
        'page_obj': page_obj
    }
    return render(request,'api/veterinary.html', context)


# def test_slider(request):
#     return render(request, 'api/test_slider.html')