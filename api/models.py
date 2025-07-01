from unicodedata import category
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class Category(models.Model):
    """Model representing product categories in the system."""
    class Meta:
        verbose_name_plural = 'category'
    type = models.CharField(max_length=200)
    description = models.TextField()
    svg_file = models.FileField(upload_to="svgs/", blank=True)  # Store in /media/svgs/
    is_medicated = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)  # Optional URL field for category

    def __str__(self):
        """String representation of the Category model."""
        return self.type


class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = 'sub category'
        
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField(upload_to="svgs/", blank=True)
    

    def __str__(self):
        """String representation of the SubCategory model."""
        return self.type

def default_subcategories():
    return list(SubCategory.objects.filter(type="other").values_list('id', flat=True))

class Product(models.Model):
    """Model representing products in the system."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    attributes = models.JSONField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ManyToManyField(SubCategory,blank=False, default=default_subcategories)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_medicated = models.BooleanField(default=False)
    is_customized = models.BooleanField(default=False)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    

    def __str__(self):
        """String representation of the Product model."""
        return self.name


class Client(models.Model):
    """Model representing clients in the system."""

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="clients/", null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Client model."""
        return self.name


class FAQ(models.Model):
    """Model representing frequently asked questions in the system."""

    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        """String representation of the FAQ model."""
        return self.question


class Testimonial(models.Model):
    """Model representing testimonials in the system."""

    customer_name = models.CharField(max_length=200)
    feedback = models.TextField()
    image = models.ImageField(upload_to="testimonials/", null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Testimonial model."""
        return self.customer_name


class Tag(models.Model):
    """Model representing tags in the system."""

    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        """Override save method to automatically generate slug from name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the Tag model."""
        return self.name


class BlogPost(models.Model):
    """Model representing blog posts in the system."""
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    intro = models.CharField(max_length=100, null=True)
    content = HTMLField()
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="blog_posts/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the BlogPost model."""
        return self.title

    def __save__(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class JobApplications(models.Model):
    """Model representing job applications in the system."""
    job_id = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    dob = models.DateField(blank=True, null=True)
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)
    job_position = models.ForeignKey('JobPosition', on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the JobApplications model."""
        return f"{self.name} - {self.job_position.position}"
# Create your models here.
class Job(models.Model):
    """Model representing job postings in the system."""

    title = models.ForeignKey('JobPosition', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    experience = models.IntegerField()
    openings = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        """String representation of the Job model."""
        return self.title.position

class JobPosition(models.Model):
    """Model representing job positions in the system."""

    position = models.CharField(max_length=200)
    def __str__(self):
        """String representation of the JobPosition model."""
        return self.position



class WebsiteImages(models.Model):
    class Meta:
        verbose_name_plural = 'Website Images'

    home_carousel_1 = models.FileField(upload_to='home_carousels', null=True, blank=True)
    home_carousel_2 = models.FileField(upload_to='home_carousels', null=True, blank=True)
    home_carousel_3 = models.FileField(upload_to='home_carousels', null=True, blank=True)
    about_hero = models.FileField(upload_to='about_us', null=True, blank=True)
    about_image_1 = models.FileField(upload_to='about_us', null=True, blank=True)
    about_image_2 = models.FileField(upload_to='about_us', null=True, blank=True)
    blog_hero = models.FileField(upload_to='blog', null=True, blank=True)
    career_hero = models.FileField(upload_to='career', null=True, blank=True)
    product_catalog_link = models.URLField(null=True, blank=True)
    know_more_about_us_link = models.URLField(null=True, blank=True)
    rnd_hero = models.FileField(upload_to='rnd_page_images', null=True, blank=True)
    formulation_hero = models.FileField(upload_to='formulation_page_images', null=True, blank=True)
    third_party_hero = models.FileField(upload_to='third_party_page_images', null=True, blank=True)
    private_labelling_hero = models.FileField(upload_to='private_labelling', null=True, blank=True)
    face_care_hero = models.FileField(upload_to='face_care', null=True, blank=True)
    face_care_image_1 = models.FileField(upload_to='face_care', null=True, blank=True)
    hair_care_hero = models.FileField(upload_to='hair_care', null=True, blank=True)
    hair_care_image_1 = models.FileField(upload_to='hair_care', null=True, blank=True)
    body_care_hero = models.FileField(upload_to='body_care', null=True, blank=True)
    body_care_image_1 = models.FileField(upload_to='body_care', null=True, blank=True)
    medicated_image_1 = models.FileField(upload_to='medicated', null=True, blank=True)
    medicated_image_2 = models.FileField(upload_to='medicated', null=True, blank=True)
    medicated_image_3 = models.FileField(upload_to='medicated', null=True, blank=True)
    medicated_image_4 = models.FileField(upload_to='medicated', null=True, blank=True)
    medicated_image_5 = models.FileField(upload_to='medicated', null=True, blank=True)
    mens_grooming_hero = models.FileField(upload_to='mens_grooming', null=True, blank=True)
    mens_grooming_image_1 = models.FileField(upload_to='mens_grooming', null=True, blank=True)
    intimate_care_hero = models.FileField(upload_to='intimate_care', null=True, blank=True)
    intimate_care_image_1 = models.FileField(upload_to='intimate_care', null=True, blank=True)
    mother_care_hero = models.FileField(upload_to='mother_care', null=True, blank=True)
    mother_care_image_1 = models.FileField(upload_to='mother_care', null=True, blank=True)
    veterinary_hero = models.FileField(upload_to='veterinary', null=True, blank=True)
    veterinary_image_1 = models.FileField(upload_to='veterinary', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
