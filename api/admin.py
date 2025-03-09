from django.contrib import admin
from .models import Category, Product, Client, FAQ, Testimonial, Tag, BlogPost
from import_export import resources
from import_export.admin import ImportExportModelAdmin
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'type', 'description')

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ( 'type', 'description')
    search_fields = ( 'type', 'description')
    list_filter = ('type', 'description')
    resource_class = CategoryResource
    list_per_page = 10

class ProductResource(resources.ModelResource):
    class Meta:
        fields = ('name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
        model = Product

class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
    search_fields = ('name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
    list_filter = ('name', 'description', 'category', 'image', 'is_featured', 'created_at', 'updated_at', 'attributes')
    resource_class = ProductResource
    list_per_page = 10

class ClientResource(resources.ModelResource):
    class Meta:
        fields = ('name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
        model = Client

class ClientAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('name', 'description', 'image', 'is_featured', 'created_at', 'updated_at')
    resource_class = ClientResource
    list_per_page = 10

class FAQResource(resources.ModelResource):
    class Meta:
        fields = ('question', 'answer', 'created_at', 'updated_at')
        model = FAQ

class FAQAdmin(ImportExportModelAdmin):
    list_display = ( 'question', 'answer', 'created_at', 'updated_at')
    search_fields = ( 'question', 'answer', 'created_at', 'updated_at')
    list_filter = ('question', 'answer', 'created_at', 'updated_at')
    resource_class = FAQResource
    list_per_page = 10

class TestimonialResource(resources.ModelResource):
    class Meta:
        fields = ('customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
        model = Testimonial

class TestimonialAdmin(ImportExportModelAdmin):
    list_display = ('customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
    search_fields = ('customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('customer_name', 'feedback', 'image', 'is_featured', 'created_at', 'updated_at')
    resource_class = TestimonialResource
    list_per_page = 10

class TagResource(resources.ModelResource):
    class Meta:
        fields = ('slug', 'name')
        model = Tag

class TagAdmin(ImportExportModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ('slug', 'name')
    list_filter = ('slug', 'name')
    resource_class = TagResource
    list_per_page = 10

class BlogPostResource(resources.ModelResource):
    class Meta:
        fields = ('title', 'content', 'created_at', 'updated_at','tags_display')
        model = BlogPost

class BlogPostAdmin(ImportExportModelAdmin):
    list_display = ('title', 'content', 'created_at', 'updated_at','tags_display')
    search_fields = ('title', 'content', 'created_at', 'updated_at','tags')
    list_filter = ( 'title', 'content', 'created_at', 'updated_at','tags')
    resource_class = BlogPostResource
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