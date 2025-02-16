from rest_framework import serializers
from .models import Category, Product, Client, FAQ, Testimonial, Tag, BlogPost

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        """Meta class to configure the CategorySerializer."""
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Product model."""
    class Meta:
        """Meta class to configure the ProductSerializer."""
        model = Product
        fields = "__all__"
    
    

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
    class Meta:
        """Meta class to configure the TestimonialSerializer."""
        model = Testimonial
        fields = "__all__"

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Tag model."""
    class Meta:
        """Meta class to configure the TagSerializer."""
        model = Tag
        fields = "__all__"

class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the BlogPost model."""
    class Meta:
        """Meta class to configure the BlogPostSerializer."""
        model = BlogPost
        fields = "__all__"
        

        
        
        
        