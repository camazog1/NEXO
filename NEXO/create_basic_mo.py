
import os


try:
    import polib
    print("Usando polib para generar el archivo .mo...")
    
    
    os.makedirs('NEXO/locale/es/LC_MESSAGES', exist_ok=True)
    
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': 'NEXO 1.0',
        'Report-Msgid-Bugs-To': '',
        'POT-Creation-Date': '2024-06-15 12:00+0000',
        'PO-Revision-Date': '2024-06-15 12:00+0000',
        'Last-Translator': '',
        'Language-Team': '',
        'Language': 'es',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding': '8bit',
        'Plural-Forms': 'nplurals=2; plural=(n != 1);',
    }
    
    
    translations = {
        
        "HOME": "INICIO",
        "MENU": "MENÚ",
        "LOGIN": "INICIAR SESIÓN",
        "SIGNUP": "REGISTRARSE",
        "DASHBOARD": "PANEL DE CONTROL",
        "LOGOUT": "CERRAR SESIÓN",
        
        
        "NEXO Colombia: Reinventando la ropa interior masculina": "NEXO Colombia: Reinventando la ropa interior masculina",
        "Home Page": "Página de Inicio",
        "Product List": "Lista de Productos",
        "Product Create": "Crear Producto",
        "Product Update": "Actualizar Producto",
        "Product Delete": "Eliminar Producto",
        "Product Detail": "Detalle del Producto",
        
        
        "Discover elegance": "Descubre la elegancia",
        "Explore": "Explora",
        "Our Styles": "Nuestros Estilos",
        "Comfort, elegance and economy here": "Comodidad, elegancia y economía aquí",
        "Buy Now!": "¡Compra Ahora!",
        "Don't have an account?": "¿No tienes una cuenta?",
        "Create one here": "Crea una aquí",
        
        
        "Log In": "Iniciar sesión",
        "Username": "Nombre de usuario",
        "Password": "Contraseña",
        "Sign Up": "Registrarse",
        "First Name": "Nombre",
        "Last Name": "Apellido",
        "Email": "Correo electrónico",
        "User Type": "Tipo de usuario",
        "Final User": "Usuario final",
        "Administrator": "Administrador",
        "Admin": "Administrador",
        "Special Admin Password": "Contraseña especial de administrador",
        "Create Account": "Crear cuenta",
        "Already have an account?": "¿Ya tienes una cuenta?",
        "Log in here.": "Inicia sesión aquí.",
        
        # Productos
        "All Products": "Todos los Productos",
        "Search by name": "Buscar por nombre",
        "Sort": "Ordenar",
        "Price: Low to High": "Precio: Menor a Mayor",
        "Price: High to Low": "Precio: Mayor a Menor",
        "Alphabetical Order": "Orden Alfabético",
        "Search": "Buscar",
        "No image available": "No hay imagen disponible",
        "Ref": "Ref",
        "Price": "Precio",
        "View Details": "Ver Detalles",
        "Popular": "Popular",
        "New": "Nuevo",
        "Discontinued": "Descontinuado",
        "No products found": "No se encontraron productos",
        "No products found related to your search.": "No se encontraron productos relacionados con tu búsqueda.",
        
        # Detalles de producto
        "Main Image": "Imagen Principal",
        "Product Image": "Imagen del Producto",
        "Product": "Producto",
        "Product Details": "Detalles del Producto",
        
        # Dashboard
        "Create New Product": "Crear Nuevo Producto",
        "ID": "ID",
        "Title": "Título",
        "Actions": "Acciones",
        "Edit": "Editar",
        "Delete": "Eliminar",
        "No products found.": "No se encontraron productos.",
        "Create Product": "Crear Producto",
        "Images": "Imágenes",
        "Save": "Guardar",
        "Update Product": "Actualizar Producto",
        "Update": "Actualizar",
        "Delete Product": "Eliminar Producto",
        "Are you sure you want to delete the product": "¿Estás seguro de que deseas eliminar el producto",
        "Yes, Delete": "Sí, Eliminar",
        "Cancel": "Cancelar",
        
        # Formularios
        "Reference": "Referencia",
        "Description": "Descripción",
        "Price (COP)": "Precio (COP)",
        "Price (USD)": "Precio (USD)",
        "Popular Product": "Producto Popular",
        "New Product": "Producto Nuevo",
        "Discontinued Product": "Producto Descontinuado",
        
        # Mensajes
        "The special admin password is incorrect.": "La contraseña especial para administrador es incorrecta.",
        "Invalid credentials": "Credenciales inválidas",
        "Product created successfully!": "¡Producto creado exitosamente!",
        "Product updated successfully!": "¡Producto actualizado exitosamente!",
        "Product deleted successfully!": "¡Producto eliminado exitosamente!",
        "User must have an email address": "El usuario debe tener un correo electrónico",
        
        # URLs
        "admin/": "administrador/",
        "users/": "usuarios/",
        "dashboard/": "panel-control/",
        
        # Footer
        "&copy; 2025 NEXO. All rights reserved.": "&copy; 2025 NEXO. Todos los derechos reservados."
    }
    
    # Añadir las entradas al archivo .po
    for original, translation in translations.items():
        entry = polib.POEntry(
            msgid=original,
            msgstr=translation,
            occurrences=[('django', '1')]
        )
        po.append(entry)
    
    # Guardar los archivos .po y .mo
    po_file = 'NEXO/locale/es/LC_MESSAGES/django.po'
    mo_file = 'NEXO/locale/es/LC_MESSAGES/django.mo'
    
    po.save(po_file)
    po.save_as_mofile(mo_file)
    
    print(f"Archivos creados: {po_file} y {mo_file}")
    print(f"Se incluyeron {len(translations)} traducciones.")
    
except ImportError:
    print("Error: polib no está instalado.")
    print("Para instalar polib, ejecuta: pip install polib")
    print("\nEste script requiere polib para funcionar correctamente.")
    print("El uso de métodos alternativos para generar el archivo .mo ha causado problemas.")
    exit(1) 