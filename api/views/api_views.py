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

from ..utils import send_contact_mail


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


def send_email_handler(subject, recipient_email, html_content,attachment=None):

    # Fallback plain text version
    text_content = strip_tags(html_content)

    # Send email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[recipient_email,]
    )
    email.attach_alternative(html_content, "text/html")
    if attachment:
        filename, content, mimetype = attachment
        email.attach(filename, content, mimetype)
    email.send()
    return f"Email sent to {recipient_email}"


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
        contact_no = request.POST.get('request-phone', '').strip()
        message = request.POST.get('request-message', '').strip()
        quantity = request.POST.get('request-quantity', '').strip()
        product_name = request.POST.get('request-product', '').strip()
        customization = request.POST.get('request-customization', '').strip()
        
    
        try:
            subject="Testing For Contact Us Leads!"
            text="Congrats for sending test email with Mailtrap! \n\n"
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Contact Us Email</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f9f9f9;
                        margin: 0;
                        padding: 0;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background: #ffffff;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .email-header {{
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        text-align: center;
                    }}
                    .email-body {{
                        padding: 20px;
                    }}
                    .email-body p {{
                        margin: 10px 0;
                    }}
                    .email-footer {{
                        background-color: #f1f1f1;
                        text-align: center;
                        padding: 10px;
                        font-size: 12px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>Contact Us Submission</h1>
                    </div>
                    <div class="email-body">
                        <p>Congrats for sending a test email with Mailtrap!</p>
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Contact No:</strong> {contact_no}</p>
                        <p><strong>Product Name:</strong> {product_name}</p>
                        <p><strong>Quantity:</strong> {quantity}</p>
                        <p><strong>Customization:</strong> {customization}</p>
                        <p><strong>Message:</strong></p>
                        <p>{message}</p>
                    </div>
                    <div class="email-footer">
                        <p>This is an automated email. Please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            send_email_handler(subject, settings.EMAIL_HOST_USER, html)
            messages.success(request, 'Email sent successfully!')
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
    contact_no = request.POST.get('phone', '').strip()
    position = request.POST.get('position', '').strip()
    dob = request.POST.get('dob', '').strip()
    resume = request.FILES.get('resume', None)
    job_id=JobPosition.objects.get(position=position).id if position else None

    if job_id:
        try:
            job = Job.objects.get(id=int(job_id))
        except Job.DoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Check for duplicate applications
        if JobApplications.objects.filter(job_id=job.id, email=email).exists():
            messages.error(request, 'You have already applied for this position.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            # Save job application to DB
            job_application = JobApplications(
                job_id=job,
                name=name,
                email=email,
                phone=contact_no,
                dob=dob,
                resume=resume,
                job_position=JobPosition.objects.get(position=position)
            )
            job_application.save()

            # Prepare HTML content for email

            # Read file content
            if resume:
                attachment = (
                    resume.name,
                    resume.read(),
                    resume.content_type
                )
            else:
                attachment = None

            # Send email to admin
            send_email_handler(
                subject=f"New Job Application: {name} - {position}",
                recipient_email=settings.EMAIL_HOST_USER,  # Change as needed
                html_content=html,
                attachment=attachment
            )

            messages.success(request, 'Your application has been submitted successfully.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while submitting your application. Please try again later.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        messages.error(request, 'Invalid job. Please try again.')
        return redirect(request.META.get('HTTP_REFERER', '/'))