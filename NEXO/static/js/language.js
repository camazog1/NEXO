/**
 * Script para manejar el cambio de idioma
 * Este script se asegura que el cambio de idioma funcione correctamente
 * incluso si hay problemas con la cookie o el middleware
 */

document.addEventListener('DOMContentLoaded', function() {
  // Función principal para manejar el cambio de idioma
  function handleLanguageChange() {
    // Obtener todos los selectores de idioma (pueden existir múltiples en la página)
    const languageSelects = document.querySelectorAll('select[name="language"]');
    
    languageSelects.forEach(function(select) {
      // Mejorar el manejo del formulario cuando cambia el idioma
      select.addEventListener('change', function() {
        // Seleccionar el formulario padre
        const form = this.closest('form');
        
        // Guardar el valor seleccionado en localStorage para persistencia
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
        
        // No necesitamos submit manual aquí ya que usamos onchange en el HTML
        // El formulario ya se enviará por el atributo onchange
      });
    });
    
    // Función para corregir la URL si el idioma en la URL no coincide con el guardado
    function correctLanguageInUrl() {
      // Verificar si hay un idioma guardado en localStorage
      const savedLanguage = localStorage.getItem('selectedLanguage');
      if (!savedLanguage) return;
      
      const urlParts = window.location.pathname.split('/');
      const urlLanguage = urlParts.length > 1 ? urlParts[1] : null;
      
      // Si el idioma en la URL no coincide con el idioma guardado, redirigir
      if (urlLanguage && ['es', 'en'].includes(urlLanguage) && savedLanguage !== urlLanguage) {
        urlParts[1] = savedLanguage;
        window.location.href = urlParts.join('/');
      }
    }
    
    // Verificar la URL al cargar la página
    // Comentamos esta parte para evitar redirecciones no deseadas
    // correctLanguageInUrl();
  }
  
  // Inicializar la funcionalidad de cambio de idioma
  handleLanguageChange();
}); 