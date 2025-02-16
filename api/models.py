from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Model representing product categories in the system."""

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        """String representation of the Category model."""
        return self.type

class Product(models.Model):
    """Model representing products in the system."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    attributes = models.JSONField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        """String representation of the Product model."""
        return self.name

class Client(models.Model):
    """Model representing clients in the system."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='clients/', null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Client model."""
        return self.name
    
class FAQ(models.Model):
    """Model representing frequently asked questions in the system."""

    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the FAQ model."""
        return self.question
    
class Testimonial(models.Model):
    """Model representing testimonials in the system."""

    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=200)
    feedback = models.TextField()
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Testimonial model."""
        return self.customer_name

class Tag(models.Model):
    """Model representing tags in the system."""

    slug = models.SlugField(unique=True,blank=True)
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

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='blog_posts/', null=True, blank=True)
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
