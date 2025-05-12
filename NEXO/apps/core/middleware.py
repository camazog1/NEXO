from django.utils import translation
from django.conf import settings

class LanguageMiddleware:
    """
    Middleware para asegurar que el idioma seleccionado se active en cada solicitud.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener el idioma de la sesión si existe
        language = request.session.get('_language', None)
        
        # Si no hay idioma en la sesión, intentar obtenerlo de la cookie
        if not language:
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, None)
        
        # Si todavía no hay idioma, usar el predeterminado
        if not language:
            language = settings.LANGUAGE_CODE
        
        # Activar el idioma para esta solicitud
        translation.activate(language)
        
        # Añadir el idioma a la solicitud para referencia
        request.LANGUAGE_CODE = language
        
        # Procesar la solicitud normalmente
        response = self.get_response(request)
        
        # Asegurarse de que la respuesta tenga el idioma correcto
        response.setdefault('Content-Language', language)
        
        return response 