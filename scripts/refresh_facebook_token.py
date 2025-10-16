#!/usr/bin/env python3
"""
🔄 ACTUALIZADOR DE TOKEN FACEBOOK
Obtiene un nuevo token de acceso de larga duración
"""
import os
import webbrowser
from dotenv import load_dotenv

load_dotenv()

def generate_facebook_auth_url():
    """Generar URL de autenticación para Facebook"""
    app_id = os.getenv('FACEBOOK_APP_ID', '236030466252408')
    
    # Permisos necesarios para nuestra aplicación
    permissions = [
        'pages_show_list',
        'pages_read_engagement', 
        'pages_read_user_content',
        'public_profile'
    ]
    
    redirect_uri = "https://localhost:8000/facebook-auth"  # URI ficticia para desarrollo
    
    auth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth?"
        f"client_id={app_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={','.join(permissions)}&"
        f"response_type=token"
    )
    
    return auth_url

def instructions():
    """Mostrar instrucciones para obtener token"""
    print("🎯 INSTRUCCIONES PARA ACTUALIZAR TOKEN FACEBOOK")
    print("=" * 60)
    print("1. 🌐 Ve al Administrador de Aplicaciones de Facebook:")
    print("   https://developers.facebook.com/apps/")
    print("")
    print("2. 🔍 Busca tu aplicación: '236030466252408'")
    print("")
    print("3. ⚙️ Ve a 'Configuración' > 'Básica'")
    print("   - Anota el 'ID de la aplicación' y 'Clave secreta de la aplicación'")
    print("")
    print("4. 🔑 Ve a 'Herramientas' > 'Explorador de Graph API'")
    print("   - En 'Token de acceso', selecciona tu página")
    print("   - Copia el token generado")
    print("")
    print("5. 📝 Actualiza el archivo .env con el nuevo token:")
    print("   FACEBOOK_ACCESS_TOKEN=tu_nuevo_token_aqui")
    print("")
    print("6. 🚀 Reinicia el sistema HelioBio-Social")
    print("")
    print("💡 CONSEJO: Los tokens de página suelen durar más que los de usuario")

if __name__ == "__main__":
    print("🔄 ACTUALIZADOR DE TOKEN FACEBOOK")
    print("=" * 50)
    
    # Mostrar configuración actual
    current_token = os.getenv('FACEBOOK_ACCESS_TOKEN', 'No configurado')
    print(f"🔑 Token actual: {current_token[:20]}...{current_token[-10:]}")
    
    print("\n¿Quieres abrir el administrador de aplicaciones de Facebook? (s/n): ")
    response = input().lower()
    
    if response == 's':
        webbrowser.open("https://developers.facebook.com/apps/236030466252408/dashboard/")
        print("✅ Navegador abierto. Sigue las instrucciones arriba.")
    
    instructions()
