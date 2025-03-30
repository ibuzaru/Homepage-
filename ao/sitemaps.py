from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# サイトマップ用クラス
class StaticViewSitemap(Sitemap):
    priority = 0.7  # 優先度を少し高めに設定
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        """サイトマップに含めるページ"""
        return [
            'home',          # トップページ
            'rooms',         # 部屋案内
            'faq',           # FAQ
            'supermarket',   # アクセス
            'sightseeing',   # 観光
            'howtostay',     # 宿泊方法
            'kiyaku',        # 利用規約
        ]

    def location(self, item):
        return reverse(item)
