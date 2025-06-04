from unicodedata import category
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class Category(models.Model):
    """Model representing product categories in the system."""

    type = models.CharField(max_length=200)
    description = models.TextField()
    svg_file = models.FileField(upload_to="svgs/", blank=True)  # Store in /media/svgs/

    def __str__(self):
        """String representation of the Category model."""
        return self.type


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField()
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


# Create your models here.
class Job(models.Model):
    """Model representing job postings in the system."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    experience = models.IntegerField()
    openings = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        """String representation of the Job model."""
        return self.title

class JobPosition(models.Model):
    """Model representing job positions in the system."""

    position = models.CharField(max_length=200)
    def __str__(self):
        """String representation of the JobPosition model."""
        return self.position
