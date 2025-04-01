from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = {
        'home': 1.0,
        'about': 0.8,
        'facilities': 0.8,
        'access': 0.6,
        'contact': 0.6,
    }
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'facilities', 'access', 'contact']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return '2025-04-01'  # ここは動的に更新可能
