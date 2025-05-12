from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
import re

# Create your views here.
class Home(TemplateView):
    template_name = 'core/home.html'

# Vista personalizada para cambiar el idioma (sobrecarga la vista de Django)
def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', settings.LANGUAGE_CODE)
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        
        # Asegura que el idioma esté en la lista de idiomas disponibles
        if language in [lang[0] for lang in settings.LANGUAGES]:
            # Establecer el idioma en la sesión
            translation.activate(language)
            # En Django 5.0, usamos directamente la clave de sesión
            request.session['_language'] = language
            
            # Eliminar prefijo de idioma actual si existe (ejemplo: /en/path o /es/path)
            current_path_match = re.match(r'^/([a-z]{2})(/.*)?$', next_url)
            if current_path_match:
                # Si ya tiene un prefijo de idioma, lo eliminamos para construir la ruta base
                path_without_lang = current_path_match.group(2) or '/'
                next_url = f'/{language}{path_without_lang}'
            else:
                # Si no tiene prefijo, aseguramos que la URL comience con / y añadimos el idioma
                if not next_url.startswith('/'):
                    next_url = '/' + next_url
                next_url = f'/{language}{next_url}' if next_url != '/' else f'/{language}/'
            
            response = HttpResponseRedirect(next_url)
            
            # Establecer la cookie de idioma
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, 
                language,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )
            
            return response
            
    # Si algo falló, redirigimos a la página de inicio
    return HttpResponseRedirect('/')