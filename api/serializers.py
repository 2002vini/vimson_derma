from os import replace
from django.forms import SlugField
from rest_framework import serializers
from .models import Category, Job, JobApplications, JobPosition, Product, Client, FAQ, Testimonial, Tag, BlogPost

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Category model."""
    svg_file = serializers.SerializerMethodField()
    class Meta:
        """Meta class to configure the CategorySerializer."""
        model = Category
        fields = "__all__"
    def get_svg_file(self, obj):
        """Removes base URL from the `svg_file` field."""
        if obj.svg_file:
            return obj.svg_file.url.replace('http://127.0.0.1:8000', '')  # Modify URL
        return None  # Return None if no file exists
class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the SubCategory model."""
    class Meta:
        """Meta class to configure the SubCategorySerializer."""
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    category=serializers.SlugRelatedField(read_only=True, slug_field="type")
    subcategory = serializers.SlugRelatedField(many=True, read_only=True, slug_field="type")
    is_medicated = serializers.BooleanField(default=False)
    is_customized = serializers.BooleanField(default=False)
    tagline = serializers.CharField( allow_blank=True, required=False)
    
    """Serializer for the Product model."""
    class Meta:
        """Meta class to configure the ProductSerializer."""
        model = Product
        fields = "__all__"
    def get_image(self, obj):
        """Removes base URL from the `image` field."""
        if obj.image:
            print("removing base url from product")
            return obj.image.url.replace('http://127.0.0.1:8000', '')
    def get_subcategory(self, obj):
        """Returns a list of subcategory names."""
        subcategories = obj.subcategory.all()
        return [subcategory.type for subcategory in subcategories]

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Client model."""
    class Meta:
        """Meta class to configure the ClientSerializer."""
        model = Client
        fields = "__all__"

class FAQSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the FAQ model."""
    class Meta:
        """Meta class to configure the FAQSerializer."""
        model = FAQ
        fields = "__all__"

class TestimonialSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Testimonial model."""
    image=serializers.SerializerMethodField()
    updated_at=serializers.SerializerMethodField()
    class Meta:
        """Meta class to configure the TestimonialSerializer."""
        model = Testimonial
        fields = "__all__"
    def get_image(self, obj):
        """Removes base URL from the `image` field."""
        if obj.image:
            print("removing base url from testimonial")
            return obj.image.url.replace('http://127.0.0.1:8000', '')  # Modify URL
        return None  # Return None if no file exists
    def get_updated_at(self, obj):
        """Returns updated_at in a human-readable format."""
        return obj.updated_at.strftime("%B %d, %Y")  # Format date

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Tag model."""
    class Meta:
        """Meta class to configure the TagSerializer."""
        model = Tag
        fields = "__all__"

class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for the BlogPost model."""   
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    updated_at=serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        """Returns updated_at in a human-readable format."""
        return obj.updated_at.strftime("%B %d, %Y")  # Format date
  
    class Meta:
        """Meta class to configure the BlogPostSerializer."""
        model = BlogPost
        fields = "__all__"
        

class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the SubCategory model."""
    category = serializers.SerializerMethodField()
    class Meta:
        """Meta class to configure the SubCategorySerializer."""
        model = Category
        fields = "__all__"
    def get_category(self, obj):
        """Returns the category name."""
        return obj.category.type

class JobSerializer(serializers.ModelSerializer):
    """Serializer for the Job model."""
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='position'
    )   
    class Meta:
        """Meta class to configure the JobSerializer."""
        model=Job
        fields = "__all__"

class JobPositionSerializer(serializers.ModelSerializer):
    """Serializer for the JobPosition model."""
    class Meta:
        model=JobPosition
        fields = "__all__"
  

class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for the JobPosition model."""
    job = serializers.SlugRelatedField(read_only=True, slug_field="id")
    
    class Meta:
        """Meta class to configure the JobPositionSerializer."""
        model = JobApplications
        fields = "__all__"
