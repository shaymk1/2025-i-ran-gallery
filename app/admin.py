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


admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(About)
admin.site.register(Blog, BlogAdmin)
