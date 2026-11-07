from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class PublicPagesSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ['login_page_customer']

    def location(self, item):
        return reverse(item)
