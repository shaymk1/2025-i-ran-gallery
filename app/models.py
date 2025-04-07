from tabnanny import verbose
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    month = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    race = models.IntegerField()
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["-id"]

    # ensures that the slug is autaomatically generated from the month and venue fields
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.month + "-" + self.venue)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.month} - {self.venue}"


class Photo(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="photos"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photos/")

    class Meta:
        verbose_name_plural = "Photos"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="about/")

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField("Category", related_name="blogs")

    class Meta:
        ordering = ["-date_created"]
        verbose_name_plural = "Blogs"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
