from django.contrib import admin
from .models import Category, JobApplications, Product, Client, FAQ, Testimonial, Tag, BlogPost, SubCategory, Job, JobPosition
from tinymce.widgets import TinyMCE
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget, JSONWidget
from import_export.admin import ImportExportModelAdmin


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'type', 'description')

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ( 'id','type', 'description')
    search_fields = ( 'id','type', 'description')
    list_filter = ('id','type', 'description')
    resource_class = CategoryResource
    list_per_page = 10

class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )

    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory',
        widget=ManyToManyWidget(SubCategory, field='name', separator=',')
    )

    attributes = fields.Field(
        column_name='attributes',
        attribute='attributes',
        widget=JSONWidget()
    )

    class Meta:
        model = Product
        import_id_fields = ('name',)
        fields = (
            'name',
            'description',
            'category',
            'subcategory',
            'image',
            'is_featured',
            'created_at',
            'updated_at',
            'attributes',
            'is_medicated',
            'is_customized',
            'tagline',
        )
        
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

    list_display = (
        'name', 'category', 'is_featured', 'is_medicated',
        'is_customized', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'description', 'tagline')
    list_filter = ('category', 'is_featured', 'is_medicated', 'is_customized', 'created_at')
    list_per_page = 20
   
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
        fields = ('question', 'answer', 'created_at', 'updated_at','is_featured')
        model = FAQ

class FAQAdmin(ImportExportModelAdmin):
    list_display = ( 'question', 'answer', 'created_at', 'updated_at','is_featured')
    search_fields = ( 'question', 'answer', 'created_at', 'updated_at','is_featured')
    list_filter = ('question', 'answer', 'created_at', 'updated_at','is_featured')
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
        formfield_overrides = {
            'content': {
                'widget': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            },
        }
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

class SubCategoryResource(resources.ModelResource):
    class Meta:
        fields = ('type', 'description', 'category')
        model = SubCategory
class SubCategoryAdmin(ImportExportModelAdmin):
    list_display = ('type', 'description', 'category')
    search_fields = ('type', 'description', 'category')
    list_filter = ('type', 'description', 'category')
    resource_class = SubCategoryResource

class JobResource(resources.ModelResource):
    class Meta:
        fields = ('title', 'description', 'created_at', 'experience', 'openings','location')
        model = Job
class JobAdmin(ImportExportModelAdmin):
    list_display = ('title', 'description', 'created_at', 'experience', 'openings', 'location')
    search_fields = ('title', 'description', 'created_at', 'experience', 'openings', 'location')
    list_filter = ('title', 'description', 'created_at', 'experience', 'openings', 'location')
    resource_class = JobResource
    list_per_page = 10

class JobPositionResource(resources.ModelResource):
    class Meta:
        fields = ('position',)
        model = JobPosition

class JobApplicationResource(resources.ModelResource):
    class Meta:
        fields = ('job_id', 'name', 'email', 'phone', 'dob', 'resume', 'job_position', 'applied_at')
        model = JobApplications

class JobApplicationAdmin(ImportExportModelAdmin):
    list_display = ('job_id', 'name', 'email', 'phone', 'dob', 'resume', 'job_position', 'applied_at')
    search_fields = ('job_id__title', 'name', 'email', 'phone', 'dob', 'resume', 'job_position__position')
    list_filter = ('job_id__title', 'name', 'email', 'phone', 'dob', 'resume', 'job_position__position')
    resource_class = JobApplicationResource
    list_per_page = 10

class JobPositionAdmin(ImportExportModelAdmin):
    list_display = ('position',)
    search_fields = ('position',)
    list_filter = ('position',)
    resource_class = JobPositionResource
    def __str__(self):
        return self.position


# admin.site.register(JobPosition, JobPositionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplications, JobApplicationAdmin)
admin.site.register(JobPosition, JobPositionAdmin)
# admin.site.register(JobPosition, JobPositionAdmin)