"""
URL configuration for NEXO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import redirect
from apps.product.views import api_products
from apps.core.views import set_language

# Función para redirigir a la URL con prefijo de idioma
def home_redirect(request):
    return redirect(f'/{settings.LANGUAGE_CODE}/')

# URLs no traducibles (estáticos y selector de idioma)
urlpatterns = [
    # Redirección a la página de inicio con prefijo de idioma
    path('', home_redirect, name='home_redirect'),
    # Selector de idioma usando nuestra vista personalizada
    path('set-language/', set_language, name='set_language'),
    # Documentación de la API (no traducible para garantizar acceso consistente)
    path('api/docs/', TemplateView.as_view(template_name='api_docs.html'), name='api_docs'),
    # API endpoint para productos
    path('api/products/', api_products, name='api_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs traducibles - Todas las URLs incluirán el prefijo de idioma
urlpatterns += i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.product.urls')),
    path(_('users/'), include('apps.users.urls')),
    path(_('dashboard/'), include('apps.dashboard.urls')),
    # Mostrar siempre el prefijo de idioma, incluso para el idioma predeterminado
    prefix_default_language=True,
)

# Archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)