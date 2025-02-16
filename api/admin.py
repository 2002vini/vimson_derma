from django.contrib import admin
from .models import Category, Product, Client, FAQ, Testimonial, Tag, BlogPost

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'description')
    search_fields = ('id', 'type', 'description')
    list_filter = ('id', 'type', 'description')
    list_per_page = 10

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
    search_fields = ('id', 'name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
    list_filter = ('id', 'name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
    list_per_page = 10

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('id', 'name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
    list_per_page = 10

class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'created_at', 'updated_at')
    search_fields = ('id', 'question', 'answer', 'created_at', 'updated_at')
    list_filter = ('id', 'question', 'answer', 'created_at', 'updated_at')
    list_per_page = 10

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
    search_fields = ('id', 'customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('id', 'customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
    list_per_page = 10

class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ('slug', 'name')
    list_filter = ('slug', 'name')
    list_per_page = 10

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at','tags_display')
    search_fields = ('id', 'title', 'content', 'created_at', 'updated_at','tags')
    list_filter = ('id', 'title', 'content', 'created_at', 'updated_at','tags')
    list_per_page = 10

    def tags_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tags_display.short_description = 'Tags'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)