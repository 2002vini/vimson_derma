from urllib import request
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from ..models import Category, Product, Client, FAQ, Testimonial, Tag, BlogPost
from ..serializers import CategorySerializer, ProductSerializer, ClientSerializer, FAQSerializer, TestimonialSerializer, TagSerializer, BlogPostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status


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

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the Product model."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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



