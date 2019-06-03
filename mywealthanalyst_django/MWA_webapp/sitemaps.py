from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9
    protocol = 'http'

    def items(self):
        return( ['dashboard','landingpage'] )

    def location(self, item):
        return( reverse(item) )
