from django.http import HttpResponse


def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /stationary/
Disallow: /customer/
Disallow: /notifications/
Disallow: /change-password/
Disallow: /logout/
Disallow: /ping

Sitemap: https://wis-stationary.onrender.com/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')
