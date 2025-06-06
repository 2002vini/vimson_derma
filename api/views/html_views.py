from turtle import position
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator


from api.serializers import CategorySerializer, JobPositionSerializer, JobSerializer, SubCategorySerializer, TagSerializer,TestimonialSerializer,ProductSerializer,BlogPostSerializer
from ..models import BlogPost, Category, Job, JobPosition, SubCategory, Tag,Testimonial,Product,Category


def index(request):
    categories=Category.objects.all()
    serialized_categories = CategorySerializer(categories, many=True,context={'request':request}).data 
    mid_index = len(serialized_categories) // 2
    categories_section_1 = serialized_categories[:mid_index]  # First half
    categories_section_2 = serialized_categories[mid_index:]  # Second half
    testimonials=Testimonial.objects.all().filter(is_featured=True).order_by('updated_at')
    serialized_testimonials = TestimonialSerializer(testimonials, many=True,context={'request':request}).data
    print("serialized testimonials are: ", serialized_testimonials)
    grouped_testimonials = [serialized_testimonials[i:i+3] for i in range(0, len(serialized_testimonials), 3)]  # Split into groups of 3


    return render(request, 'index.html',{'category_section_1':categories_section_1, 'category_section_2':categories_section_2,'grouped_testimonials':grouped_testimonials,'testimonials':serialized_testimonials})

def about(request):
    return render(request, 'about.html')

def service(request):
    categories = Category.objects.all()
    serialized_categories=CategorySerializer(categories, many=True,context={'request':request}).data
    print("serialized categories:",serialized_categories)
    return render(request,'service.html',{'products':serialized_categories})
def manafacturing(request):
    categories = Category.objects.all()
    serialized_categories=CategorySerializer(categories, many=True,context={'request':request}).data
    testimonials=Testimonial.objects.all()
    serialized_testimonials = TestimonialSerializer(testimonials, many=True,context={'request':request}).data
    return render(request,'manafacturing.html',{'products':serialized_categories,'testimonials':serialized_testimonials})

def blogs(request):
    selected_tags=request.GET.get('tags')
    categories = Category.objects.all()
    blogs=BlogPost.objects.all()
    tags=Tag.objects.all()

    serialized_blog_post=BlogPostSerializer(blogs,many=True,context={'request':request}).data
    print("serialized blogs are: ", serialized_blog_post)
    
    return render(request,'blogs.html',
                  {'blogs':serialized_blog_post})

def blog_detail(request, id):
    blog = BlogPost.objects.all().get(id=id)
    blog_serailized = BlogPostSerializer(blog, context={'request': request}).data
    print("serialized blog is: ", blog_serailized)
    return render(request, 'blog_detail.html', {'blog': blog_serailized})

def facecare(request):
    # Fetch all the products that need to be displayed
    products=Product.objects.all().filter(is_featured=False,category=4).order_by('updated_at')
    selected_tag = request.GET.get('filter')
    print("selected tag is: ", selected_tag)
    if selected_tag:
        products = products.filter(subcategory__type=selected_tag)  # Assuming 'tags' is a ManyToManyField in Product model
        print(f"Filtering products by tag: {selected_tag}")
    #Fetch the page number from the request 
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 5)
    page_obj = paginator.get_page(page_number)
    featured_products=Product.objects.all().filter(is_featured=True,category=4).order_by('updated_at')
    serialized_products = ProductSerializer(page_obj.object_list, many=True, context={'request': request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category=4), many=True,context={'request':request}).data
    return render(request,'facecare.html',{'products':serialized_products,'page_obj':page_obj,'subcategory':serialized_sub_categories,'featured_products':serialized_featured_products})

def haircare(request):
    selected_subcategory = request.GET.get('subcategory')
    featured_products=Product.objects.all().filter(is_featured=True,category=3).order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category=3).order_by('updated_at')
    if selected_subcategory:
        products = products.filter(subcategory__type=selected_subcategory)
        print("selected subcategory is: ", selected_subcategory)
    serialized_products=ProductSerializer(products,many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category=3), many=True,context={'request':request}).data
    return render(request,'haircare.html',{'products':serialized_products,'featured_products':serialized_featured_products,'subcategory':serialized_sub_categories})

def bodycare(request):
    featured_products=Product.objects.all().filter(is_featured=True,category=9).order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category=9).order_by('updated_at')
    serialized_products=ProductSerializer(products,many=True,context={'request':request}).data
    serialized_featured_products=ProductSerializer(featured_products,many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all().filter(category=9), many=True,context={'request':request}).data
    return render(request,'bodycare.html',{'products':serialized_products,'subcategory':serialized_sub_categories,'featured_products':serialized_featured_products})

def mens_grooming(request):
    featured_products=Product.objects.all().filter(is_featured=True,category=9).order_by('updated_at')
    products=Product.objects.all().filter(is_featured=False,category=9).order_by('updated_at')
    serialized_products=ProductSerializer(products,many=True,context={'request':request}).data
    serialized_categories=CategorySerializer(Category.objects.all(), many=True,context={'request':request}).data
    serialized_sub_categories=SubCategorySerializer(SubCategory.objects.all(), many=True,context={'request':request}).data
    return render(request,'mens_grooming.html',{'products':serialized_products,'categories':serialized_categories,'subcategory':serialized_sub_categories})


def product_detail(request,product_id):
    product=Product.objects.get(id=product_id)
    serialized_product=ProductSerializer(product,context={'request':request}).data
    print("serialized product is: ", serialized_product)
    return render(request,'product_detail.html',{'product':serialized_product})

def careers(request):
    Jobs=Job.objects.all()
    serialized_jobs=JobSerializer(Jobs,many=True,context={'request':request}).data
    positions=JobPosition.objects.all()
    serialized_positions=JobPositionSerializer(positions,many=True,context={'request':request}).data
    
    return render(request,'careers.html',{'jobs':serialized_jobs,'positions':serialized_positions})

def career_detail(request,job_id):
    job=Job.objects.get(id=job_id)
    remaining_top_jobs=Job.objects.exclude(id=job_id).order_by('-created_at')[:3]
    serialized_job=JobSerializer(job,context={'request':request}).data
    return render(request,'career_detail.html',{'job':serialized_job,'remaining_top_jobs':remaining_top_jobs})


def innovation(request):
    blogs=BlogPost.objects.all()
    print("blogs are: ", blogs) 
    serialized_blogs=BlogPostSerializer(blogs,many=True,context={'request':request}).data
    print("serialized blogs are: ", serialized_blogs)
    return render(request,'innovation.html',{'blogs':serialized_blogs})

def research(request):
    blogs=BlogPost.objects.all()
    serialized_blogs=BlogPostSerializer(blogs,many=True,context={'request':request}).data
    return render(request,'research.html',{'blogs':serialized_blogs})