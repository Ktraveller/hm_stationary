from django.contrib.staticfiles.finders import find
from django.http import FileResponse, Http404, HttpResponse


def favicon(request):
    icon_path = find('icons/stationary1.png')
    if not icon_path:
        raise Http404('Favicon not found.')

    response = FileResponse(open(icon_path, 'rb'), content_type='image/png')
    response['Cache-Control'] = 'public, max-age=86400'
    return response


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
