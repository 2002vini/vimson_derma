from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.db.models import Q
from rest_framework import viewsets

from vimson_derma import settings
from ..models import Category, Job, JobApplications, JobPosition, Product, Client, FAQ, SubCategory, Testimonial, Tag, BlogPost
from ..serializers import CategorySerializer, ProductSerializer, ClientSerializer, FAQSerializer, SubCategorySerializer, TestimonialSerializer, TagSerializer, BlogPostSerializer
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.response import Response
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import mimetypes
from ..utils import send_contact_mail, send_carrier_mail, send_quote_mail


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category model."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """List all products for a category."""
        category = Category.objects.get(pk=pk)
        products = Product.objects.filter(category=category)
        product_serializer_data = ProductSerializer(products, many=True,context={'request': request})
        return Response(product_serializer_data.data)


class SubCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the SubCategory model."""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the Product model."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """List all products for a subcategory."""
        subcategory = SubCategory.objects.get(pk=pk)
        products = Product.objects.filter(subcategory=subcategory)
        product_serializer_data = ProductSerializer(products, many=True,context={'request': request})
        return Response(product_serializer_data.data)


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for the Client model."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class FAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the FAQ model."""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    """ViewSet for the Testimonial model."""
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for the Tag model."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def delete(self, request, pk=None):
        """Handle DELETE requests, allowing deletion by name."""
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response({'message': 'Tag deleted successfully'})


class BlogPostViewSet(viewsets.ModelViewSet):
    """ViewSet for the BlogPost model."""
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    
    def get_queryset(self):
        """Get the queryset for the BlogPost model with filtering and search."""
        queryset = BlogPost.objects.all()
        
        # Search functionality
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Tags filtering (existing code)
        tags = self.request.query_params.getlist('tags', None)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-created_at')
        allowed_fields = ['created_at', 'title', 'updated_at']
        if ordering.lstrip('-') in allowed_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset

    
    def list(self, request, *args, **kwargs):
        """List the BlogPost model with pagination."""
        queryset = self.get_queryset()
        
        # Pagination
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        
        # Limit the queryset
        paginated_queryset = queryset[offset:offset + limit]
        
        # Get total count
        total_count = queryset.count()
        
        serializer = self.get_serializer(paginated_queryset, many=True, context={'request': request})
        
        return Response({
            'count': total_count,
            'next': offset + limit if offset + limit < total_count else None,
            'previous': offset - limit if offset > 0 else None,
            'results': serializer.data
        })
    
    def delete(self, request, pk=None):
        """Delete the BlogPost model."""
        blog_post = BlogPost.objects.get(pk=pk)
        blog_post.delete()
        return Response({'message': 'BlogPost deleted successfully'})
    
    def update(self, request, pk=None):
        """Update the BlogPost model."""
        blog_post = BlogPost.objects.get(pk=pk)
        serializer = self.get_serializer(blog_post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@require_POST
def contact_submit(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    contact_no = request.POST.get('phone', '').strip()
    company = request.POST.get('company', '').strip()
    category = request.POST.get('category', '').strip()
    message = request.POST.get('message', '').strip()

    # Send email (or process data)
    send_contact_mail(
        email = email,
        name = name,
        company_name = company,
        phone_number = contact_no,
        category = category,
        message = message
    )
    messages.success(request, 'Form Submitted Successfully')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def quote_submit(request):
    """Handle the request for a quote."""
    if request.method == 'POST':
        name = request.POST.get('request-name', '').strip()
        email = request.POST.get('request-email', '').strip()
        company = request.POST.get('request-company', '').strip()
        contact_no = request.POST.get('request-phone', '').strip()
        message = request.POST.get('request-message', '').strip()
        quantity = request.POST.get('request-quantity', '').strip()
        product_name = request.POST.get('request-product', '').strip()
        customization = request.POST.get('request-customization', '').strip()
        
    
        try:
            send_quote_mail(
                name = name,
                email = email,
                contact_no = contact_no,
                product_name = product_name,
                quantity = quantity,
                customization = customization,
                company = company,
                message = message,
            )
            messages.success(request, 'Quotation sent successfully!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        except Exception as e:
            messages.error(request, 'An error occurred while sending the email. Please try again later.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    raise Http404("Page not found")


@require_POST
def careers_apply(request):
    """Handle the request for a job application."""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    dob = request.POST.get('dob', '').strip()
    contact_no = request.POST.get('phone', '').strip()
    position = request.POST.get('position', '').strip()
    job_id = request.POST.get('job_id', '').strip()
    resume = request.FILES.get('resume', None)

    if job_id:

        job = Job.objects.filter(id=int(job_id))
        if not job.exists():
            messages.error(request, 'Job not found.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        job = job.first()

        job_position = JobPosition.objects.filter(position=position)
        if not job_position.exists():
            messages.error(request, 'Job Position not found.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        job_position = job_position.first()


        # Check for duplicate applications
        job_application = JobApplications.objects.filter(job_id__id=job.id, email=email)
        if job_application.exists():
            messages.error(request, 'You have already applied for this position.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Save job application to DB
        job_application = JobApplications.objects.create(
            job_id=job,
            name=name,
            email=email,
            phone=contact_no,
            dob=dob,
            resume=resume,
            job_position=job_position
        )

        resume_file = job_application.resume

        with resume_file.open('rb') as f:
            file_content = f.read()

        filename = resume_file.name.split('/')[-1]
        mimetype, _ = mimetypes.guess_type(resume_file.name)
        mimetype = mimetype or "application/octet-stream"
        attachment = {
            'file_name': filename,
            'file_content': file_content,
            'content_type': mimetype
        }

        # Send email to Vimson Owners related to Application of Career
        send_carrier_mail(
            name = name,
            email = email,
            dob = dob,
            phone_number = contact_no,
            position = position,
            file_attachment = attachment,
        )

        messages.success(request, 'Your application has been submitted successfully.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, 'Invalid job. Please try again.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
