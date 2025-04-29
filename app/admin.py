from django.contrib import admin
from .models import Category, Photo, About, Blog
from django.utils.text import slugify


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("month", "venue")
    }  # Prepopulate slug in the admin form

    def save_model(self, request, obj, form, change):
        if not obj.slug:  # Only generate slug if it's not already set
            obj.slug = slugify(f"{obj.month}-{obj.venue}")
        super().save_model(request, obj, form, change)


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # Prepopulate slug in the admin form

    def save_model(self, request, obj, form, change):
        if not obj.slug:  # Only generate slug if it's not already set
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    display_tags.short_description = "Tags"


# class TagAdmin(admin.ModelAdmin):
#     prepopulated_fields = {
#         "slug": ("name", "category")
#     }  # Prepopulate slug in the admin form

#     def save_model(self, request, obj, form, change):
#         if not obj.slug:  # Only generate slug if it's not already set
#             obj.slug = slugify(f"{obj.name}-{obj.category}")
#         super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(About)
admin.site.register(Blog, BlogAdmin)
# admin.site.register(Tag, TagAdmin)
