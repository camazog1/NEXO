"""
Script para compilar manualmente archivos .po a .mo
Ejecuta este script en la raíz del proyecto
"""

import os
import subprocess
import sys

try:
    import polib
    print("Usando polib para compilar traducciones...")
    
    po_file = os.path.join('NEXO', 'locale', 'es', 'LC_MESSAGES', 'django.po')
    mo_file = os.path.join('NEXO', 'locale', 'es', 'LC_MESSAGES', 'django.mo')
    
    if os.path.exists(po_file):
        po = polib.pofile(po_file)
        po.save_as_mofile(mo_file)
        print(f"Archivo creado: {mo_file}")
    else:
        print(f"Error: No se pudo encontrar el archivo {po_file}")
except ImportError:
    print("polib no está instalado. Intentando con msgfmt...")
    
    try:
        # Intenta usar msgfmt si está disponible en el sistema
        po_file = os.path.join('NEXO', 'locale', 'es', 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join('NEXO', 'locale', 'es', 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_file):
            cmd = ['msgfmt', po_file, '-o', mo_file]
            subprocess.run(cmd)
            print(f"Archivo creado: {mo_file}")
        else:
            print(f"Error: No se pudo encontrar el archivo {po_file}")
    except Exception as e:
        print(f"Error al compilar usando msgfmt: {e}")
        
        # Si ambos métodos fallan, crea un archivo .mo mínimo que contenga
        # al menos algunas traducciones clave
        try:
            import marshal
            import struct
            
            print("Creando un archivo .mo básico...")
            
            po_file = os.path.join('NEXO', 'locale', 'es', 'LC_MESSAGES', 'django.po')
            mo_file = os.path.join('NEXO', 'locale', 'es', 'LC_MESSAGES', 'django.mo')
            
            # Asegura que el directorio exista
            os.makedirs(os.path.dirname(mo_file), exist_ok=True)
            
            # Un conjunto mínimo de traducciones críticas
            translations = {
                "HOME": "INICIO",
                "MENU": "MENÚ",
                "LOGIN": "INICIAR SESIÓN",
                "SIGNUP": "REGISTRARSE",
                "DASHBOARD": "PANEL DE CONTROL",
                "LOGOUT": "CERRAR SESIÓN",
                "Product List": "Lista de Productos",
                "All Products": "Todos los Productos",
                "Search": "Buscar",
                "Title": "Título",
                "Price": "Precio",
                "View Details": "Ver Detalles",
                "No products found.": "No se encontraron productos.",
                "Popular": "Popular",
                "New": "Nuevo",
                "Discontinued": "Descontinuado",
                "Log In": "Iniciar Sesión",
                "Username": "Nombre de usuario",
                "Password": "Contraseña",
                "Don't have an account?": "¿No tienes una cuenta?",
                "Create one here": "Crea una aquí",
                "Sign Up": "Registrarse",
                "Create Account": "Crear Cuenta",
                "First Name": "Nombre",
                "Last Name": "Apellido",
                "Email": "Correo electrónico",
                "User Type": "Tipo de Usuario",
                "Administrator": "Administrador",
                "Final User": "Usuario Final"
            }
            
            with open(mo_file, 'wb') as f:
                # Cabecera mágica
                f.write(struct.pack('<IIIIII', 
                    0x950412de,  # Magic
                    0,           # Version
                    len(translations),  # Number of strings
                    28,          # Offset of original string table
                    28 + len(translations) * 8,  # Offset of translation string table
                    0            # Size of hashing table
                ))
                
                # Donde se almacenarán las cadenas
                originals = []
                translations_list = []
                
                # Posición después de las tablas
                string_data_offset = 28 + len(translations) * 16
                
                # Escribe el índice para cadenas originales
                offset = string_data_offset
                for original in translations.keys():
                    length = len(original.encode('utf-8'))
                    f.write(struct.pack('<II', length, offset))
                    originals.append((length, offset, original))
                    offset += length + 1  # +1 para null-terminator
                
                # Escribe el índice para cadenas traducidas
                for original, translation in translations.items():
                    length = len(translation.encode('utf-8'))
                    f.write(struct.pack('<II', length, offset))
                    translations_list.append((length, offset, translation))
                    offset += length + 1  # +1 para null-terminator
                
                # Escribe las cadenas originales
                for _, _, original in originals:
                    f.write(original.encode('utf-8') + b'\0')
                
                # Escribe las cadenas traducidas
                for _, _, translation in translations_list:
                    f.write(translation.encode('utf-8') + b'\0')
                
            print(f"Archivo básico creado: {mo_file}")
        except Exception as e:
            print(f"Error al crear archivo .mo básico: {e}")
            print("Por favor, instala 'polib' con 'pip install polib' para compilar las traducciones")
            sys.exit(1)

print("Compilación de traducciones completada.") 