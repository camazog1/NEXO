/**
 * Script para manejar el cambio de idioma
 * Este script se asegura que el cambio de idioma funcione correctamente
 * incluso si hay problemas con la cookie o el middleware
 */

document.addEventListener('DOMContentLoaded', function() {
  // Función para manejar el cambio de idioma
  function handleLanguageChange() {
    // Obtener todos los selectores de idioma (pueden existir múltiples en la página)
    const languageSelects = document.querySelectorAll('select[name="language"]');
    
    languageSelects.forEach(function(select) {
      select.addEventListener('change', function() {
        // Seleccionar el formulario padre
        const form = this.closest('form');
        
        // Guardar el valor seleccionado en localStorage
        localStorage.setItem('selectedLanguage', this.value);
        
        // Asegurarse de que el campo next tiene un valor correcto
        const nextInput = form.querySelector('input[name="next"]');
        if (nextInput) {
          // Obtener la URL actual
          let currentUrl = window.location.pathname;
          
          // Si la URL comienza con un prefijo de idioma, necesitamos reemplazarlo
          const urlParts = currentUrl.split('/');
          if (urlParts.length > 1 && ['es', 'en'].includes(urlParts[1])) {
            // Reemplazar el prefijo de idioma con el nuevo idioma
            urlParts[1] = this.value;
            nextInput.value = urlParts.join('/');
          } else {
            // Si no hay prefijo, simplemente agregamos uno
            nextInput.value = '/' + this.value + currentUrl;
          }
        }
        
        // Agregar un pequeño retraso para asegurar que el formulario se procese correctamente
        setTimeout(function() {
          form.submit();
        }, 100);
      });
    });
    
    // Verificar si hay un idioma guardado en localStorage
    const savedLanguage = localStorage.getItem('selectedLanguage');
    const urlLanguage = window.location.pathname.split('/')[1];
    
    // Si el idioma en la URL no coincide con el idioma guardado, redirigir
    if (savedLanguage && urlLanguage && savedLanguage !== urlLanguage) {
      const newUrl = window.location.pathname.replace(`/${urlLanguage}/`, `/${savedLanguage}/`);
      window.location.href = newUrl;
    }
  }
  
  // Inicializar la funcionalidad de cambio de idioma
  handleLanguageChange();
}); 