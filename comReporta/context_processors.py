from django.conf import settings

def language_switcher(request):
    # Get language from session or cookie
    language = request.session.get('django_language')
    if not language:
        language = request.COOKIES.get('django_language', 'en')
    
    return {
        'LANGUAGES': settings.LANGUAGES,
        'current_language': language,
    }