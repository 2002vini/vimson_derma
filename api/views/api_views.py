from urllib import request
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from ..models import Category, Job, JobApplications, JobPosition, Product, Client, FAQ, SubCategory, Testimonial, Tag, BlogPost
from ..serializers import CategorySerializer, ProductSerializer, ClientSerializer, FAQSerializer, SubCategorySerializer, TestimonialSerializer, TagSerializer, BlogPostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import re
import mailtrap as mt

def send_mailtrap_email(name, email, contact_no, dob,resume=None):
    """Function to send an email using Mailtrap."""
    try:
        resume_content = resume.read() if resume else None
        if resume_content:
            resume_name = resume.name
            resume_mime_type = resume.content_type
            attachment = mt.Attachment(
                filename=resume_name,
                content=resume_content,
                mimetype=resume_mime_type
            )
         
        mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
        to=[mt.Address(email="hundlanivini2002@gmail.com")],
        subject="Testing For Contact Us Leads!",
        text="Congrats for sending test email with Mailtrap! \n\n",
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
                    <p><strong>Date of birth:</strong></p>
                    <p>{dob}</p>
                </div>
                <div class="email-footer">
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """,
        category="Integration Test",
        attachments=[attachment] if resume_content else []
        )
        client = mt.MailtrapClient(token="ad0bd2f3543f7375bb7dc34bd84a933b")
        response = client.send(mail)
      
        return True
    except Exception as e:
        print(f"Error creating mail object: {e}")
        return False


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
    message = request.POST.get('message', '').strip()

    # Basic validation
    if not name:
        return JsonResponse({'status': 0, 'error': '* Please Enter Name.'})

    if not re.match(r'^[a-zA-Z][a-zA-Z\s\-\,\.]*$', name):
        return JsonResponse({'status': 0, 'error': f'* Invalid Name: {name}'})

    if not email or not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
        return JsonResponse({'status': 0, 'error': '* Invalid Email ID.'})

    contact_clean = contact_no.replace('+', '')
    if not contact_clean or not re.match(r'^\d{10,15}$', contact_clean):
        return JsonResponse({'status': 0, 'error': '* Invalid Contact No.'})

    # Send email (or process data)
    try:
        mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
        to=[mt.Address(email="hundlanivini2002@gmail.com")],
        subject="Testing For Contact Us Leads!",
        text="Congrats for sending test email with Mailtrap! \n\n",
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
                    <p><strong>Message:</strong></p>
                    <p>{message}</p>
                </div>
                <div class="email-footer">
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """,
        
        category="Integration Test",
        )

        client = mt.MailtrapClient(token="ad0bd2f3543f7375bb7dc34bd84a933b")
        response = client.send(mail)

        print(response)
        print("submitted successfully")
        messages.success(request, 'Item successfully added!')

        
        return JsonResponse({'status': 1, 'message': 'Form submitted successfully'})
    except Exception as e:
        return JsonResponse({'status': 0, 'error': f'Server error: {str(e)}'})


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
        # Basic validation
        if not name:
            return JsonResponse({'status': 0, 'error': '* Please Enter Name.'})

        if not re.match(r'^[a-zA-Z][a-zA-Z\s\-\,\.]*$', name):
            return JsonResponse({'status': 0, 'error': f'* Invalid Name: {name}'})

        if not email or not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            return JsonResponse({'status': 0, 'error': '* Invalid Email ID.'})

        contact_clean = contact_no.replace('+', '')
        if not contact_clean or not re.match(r'^\d{10,15}$', contact_clean):
            return JsonResponse({'status': 0, 'error': '* Invalid Contact No.'})

        if not quantity or not re.match(r'^\d+$', quantity):
            return JsonResponse({'status': 0, 'error': '* Invalid Quantity.'})
        if not product_name:
            return JsonResponse({'status': 0, 'error': '* Please Enter Product Name.'})
        
    
        try:
            mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
            to=[mt.Address(email="hundlanivini2002@gmail.com")],
            subject="Testing For Contact Us Leads!",
            text="Congrats for sending test email with Mailtrap! \n\n",
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
                        <p><strong>Message:</strong></p>
                        <p>{message}</p>
                    </div>
                    <div class="email-footer">
                        <p>This is an automated email. Please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """,

            category="Integration Test",
            )

            client = mt.MailtrapClient(token="ad0bd2f3543f7375bb7dc34bd84a933b")
            response = client.send(mail)

            print(response)
            return JsonResponse({'status': 1, 'message': 'Form submitted successfully'})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': f'Server error: {str(e)}'})



@require_POST
def careers_apply(request):
    """Handle the request for a job application."""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    contact_no = request.POST.get('phone', '').strip()
    position = request.POST.get('position', '').strip()
    job_id = request.POST.get('job_id', '').strip()
    dob = request.POST.get('dob', '').strip()
    resume = request.FILES.get('resume', None)
    # Basic validation
    if not name:
        print("name is empty")
        return JsonResponse({'status': 0, 'error': '* Please Enter Name.'})

    if not re.match(r'^[a-zA-Z][a-zA-Z\s\-\,\.]*$', name):
        print("name is invalid")
        return JsonResponse({'status': 0, 'error': f'* Invalid Name: {name}'})

    if not email or not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
        print("email is invalid")
        return JsonResponse({'status': 0, 'error': '* Invalid Email ID.'})

    contact_clean = contact_no.replace('+', '')
    if not contact_clean or not re.match(r'^\d{10,15}$', contact_clean):
        print("contact no is invalid")
        return JsonResponse({'status': 0, 'error': '* Invalid Contact No.'})
    if not resume:
        print("resume is empty")
        return JsonResponse({'status': 0, 'error': '* Please upload your resume.'})
    if not position:
        print("position is empty")
        return JsonResponse({'status': 0, 'error': '* Please select a position to apply.'})
    
    if job_id:
        print("job id exists!")
        try:
            job = Job.objects.get(id=int(job_id))
        except Job.DoesNotExist:
            return JsonResponse({'status': 0, 'error': '* Invalid Job ID.'})
        # check if the job position is already applied for
        if JobApplications.objects.filter(job_id=job.id, email=email).exists():
            print("already applied for the same job")
            return JsonResponse({'status': 0, 'error': '* You have already applied for this job.'})
        # add job_id to the job application
        job_application=JobApplications(
            job_id=job,
            name=name,
            email=email,
            phone=contact_no,
            dob=dob,
            resume=resume,
            job_position=JobPosition.objects.get(position=position)
        )
        #todo: send email for admin
        job_application.save()
        if not send_mailtrap_email(name, email, contact_no, dob, resume):
            print("failed to send email")
            return JsonResponse({'status': 0, 'error': '* Failed to send email. Please try again later.'})
        print("data has been validated successfully")
        return JsonResponse({'status': 1, 'message': 'Form submitted successfully','success': True})
    
    # Validate if from same email we have already applied for the same position
    if JobApplications.objects.filter(email=email, job_position__position=position).exists():
        print("already applied for the same position")
        return JsonResponse({'status': 0, 'error': '* You have already applied for this position.'})
    else:
        # Save the job application
        job_application = JobApplications(
            name=name,
            email=email,
            phone=contact_no,
            dob=dob,
            resume=resume,
            job_position=JobPosition.objects.get(position=position)
        )
        job_application.save()
        send_mailtrap_email(name, email, contact_no, dob, resume)
        #todo: send email notification to admin
    print("data has been validated successfully")
    return JsonResponse({'status': 1, 'message': 'Form submitted successfully','success': True})
    # Save the resume file

