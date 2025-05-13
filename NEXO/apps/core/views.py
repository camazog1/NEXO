from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
import re
import requests
from django.http import HttpResponse
import json
from datetime import datetime

# Create your views here.
class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir tipos de cambio al contexto
        context['exchange_rates'] = get_exchange_rates()
        return context


def change_language(request):
    """Vista para cambiar el idioma de la sesión."""
    if request.method == 'POST':
        language = request.POST.get('language', settings.LANGUAGE_CODE)
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        
        # Asegura que el idioma esté en la lista de idiomas disponibles
        if language in [lang[0] for lang in settings.LANGUAGES]:
            # Activar el idioma para la solicitud actual
            translation.activate(language)
            
            # Crear una respuesta de redirección
            response = HttpResponseRedirect(next_url)
            
            # Establecer el idioma en la sesión y la cookie
            request.session['_language'] = language
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
    
    # Si es una solicitud GET o algo falló
    return redirect(request.META.get('HTTP_REFERER', '/'))

def productos_aliados(request):
    
    api_url = "http://127.0.0.1:8000/api/products/"
    
    try:
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            productos = data.get('products', [])
            
            # Obtener los tipos de cambio
            exchange_rates = get_exchange_rates()
            
            # Añadir precios convertidos a EUR y GBP para cada producto
            for producto in productos:
                if 'price_dolar' in producto:
                    # Convertir precios USD a EUR y GBP
                    precio_usd = float(producto['price_dolar'])
                    producto['price_eur'] = round(precio_usd * exchange_rates['USD_COP'] / exchange_rates['EUR_COP'], 2)
                    producto['price_gbp'] = round(precio_usd * exchange_rates['USD_COP'] / exchange_rates['GBP_COP'], 2)
            
            return render(request, 'core/productos_aliados.html', {
                'productos': productos,
                'equipo_origen': data.get('service_info', {}).get('name', 'Equipo aliado'),
                'exchange_rates': exchange_rates,
                'error': None
            })
        else:
            return render(request, 'core/productos_aliados.html', {
                'productos': [],
                'equipo_origen': None,
                'exchange_rates': get_exchange_rates(),
                'error': f'Error al obtener los productos. Código: {response.status_code}'
            })
            
    except requests.exceptions.RequestException as e:
        # En caso de error de conexión
        return render(request, 'core/productos_aliados.html', {
            'productos': [],
            'equipo_origen': None,
            'exchange_rates': get_exchange_rates(),
            'error': f'Error de conexión: {str(e)}'
        })
    except Exception as e:
        # Otros errores
        return render(request, 'core/productos_aliados.html', {
            'productos': [],
            'equipo_origen': None,
            'exchange_rates': get_exchange_rates(),
            'error': f'Error inesperado: {str(e)}'
        })

# Función para obtener el tipo de cambio actual
def get_exchange_rates():
    """
    Obtiene los tipos de cambio actuales utilizando la API de ExchangeRate-API.
    Devuelve un diccionario con las tasas para USD, EUR y GBP con respecto a COP.
    """
    try:
        # URL de la API
        api_url = "https://open.er-api.com/v6/latest/USD"
        
        # Realizar la petición a la API
        response = requests.get(api_url, timeout=5)
        
        # Verificar si la petición fue exitosa
        if response.status_code == 200:
            # Parsear los datos JSON
            data = response.json()
            
            # Verificar si los datos son válidos
            if data.get('result') == 'success':
                # Obtener las tasas para COP, EUR y GBP
                rates = {
                    'USD_COP': data['rates']['COP'],
                    'EUR_COP': data['rates']['COP'] / data['rates']['EUR'],
                    'GBP_COP': data['rates']['COP'] / data['rates']['GBP'],
                    'last_updated': data['time_last_update_utc'],
                }
                return rates
        
        # Si hay algún problema, devolver tasas predeterminadas
        return {
            'USD_COP': 4000,  # Valor predeterminado aproximado
            'EUR_COP': 4300,  # Valor predeterminado aproximado
            'GBP_COP': 5000,  # Valor predeterminado aproximado
            'last_updated': datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000"),
        }
    
    except Exception as e:
        # En caso de error, devolver tasas predeterminadas
        return {
            'USD_COP': 4000,  # Valor predeterminado aproximado
            'EUR_COP': 4300,  # Valor predeterminado aproximado
            'GBP_COP': 5000,  # Valor predeterminado aproximado
            'last_updated': datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000"),
            'error': str(e)
        }

def set_language(request):
    """Custom view to set the language in the session and cookies"""
    if request.method == 'POST':
        language = request.POST.get('language', settings.LANGUAGE_CODE)
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        
        print(f"Changing language to {language}")
        print(f"Next URL: {next_url}")
        
        # Ensure the language is in the available languages
        if language in [lang[0] for lang in settings.LANGUAGES]:
            # Activate the language for the current request
            translation.activate(language)
            
            # Parse the next_url to modify it correctly for the language change
            if next_url.startswith('/'):
                # If there's a language prefix, replace it
                parts = next_url.split('/')
                if len(parts) > 1 and parts[1] in [lang[0] for lang in settings.LANGUAGES]:
                    parts[1] = language
                    next_url = '/'.join(parts)
                else:
                    # If there's no language prefix, add it
                    next_url = f'/{language}{next_url}'
            else:
                # If it doesn't start with /, add the language prefix
                next_url = f'/{language}/{next_url}'
            
            print(f"Modified next URL: {next_url}")
            
            # Create the redirect response
            response = HttpResponseRedirect(next_url)
            
            # Set the language in the session and cookie
            request.session['_language'] = language
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
            
            print(f"Language set to {language} - redirecting to {next_url}")
            return response
    
    # For GET requests or if something went wrong
    referer = request.META.get('HTTP_REFERER', '/')
    print(f"Language set failed, redirecting to {referer}")
    return redirect(referer)