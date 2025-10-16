#!/usr/bin/env python3
"""
🔍 VERIFICADOR DE CONFIGURACIÓN FACEBOOK
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 VERIFICANDO CONFIGURACIÓN FACEBOOK...")
print("=" * 50)

# Verificar variables
app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET') 
access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
page_id = os.getenv('FACEBOOK_PAGE_ID')

print(f"📱 Facebook App ID: {'✅' if app_id else '❌'} {app_id}")
print(f"🔐 Facebook App Secret: {'✅' if app_secret else '❌'} {'*' * 10 if app_secret else ''}")
print(f"🎫 Facebook Access Token: {'✅' if access_token else '❌'} {'*' * 10 if access_token else ''}")
print(f"📄 Facebook Page ID: {'✅' if page_id else '❌'} {page_id}")

# Verificar formato del Page ID
if page_id:
    clean_page_id = page_id.strip('"')
    print(f"📄 Page ID limpio: {clean_page_id}")
    
    # Verificar si es numérico o de texto
    if clean_page_id.isdigit():
        print("📊 Tipo de Page ID: Numérico")
    else:
        print("📊 Tipo de Page ID: Nombre de página")
        print("💡 Si usas nombre de página, asegúrate de que sea exacto")

print("=" * 50)

if all([app_id, app_secret, access_token, page_id]):
    print("🎉 ¡Todas las variables están configuradas!")
    print("🚀 Ejecuta el sistema para probar la conexión")
else:
    print("❌ Faltan variables de configuración")
    print("💡 Ejecuta: python scripts/setup_tokens_interactive.py")
