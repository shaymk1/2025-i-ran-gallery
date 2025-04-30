from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Blog


class LatestPostsFeed(Feed):
    title = "In 2025 I Ran Blog"
    link = "/blog/"
    description = "Latest posts from In 2025 I Ran Blog."

    def items(self):
        return Blog.objects.order_by("-date_created")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse("blog_detail", args=[item.slug])
