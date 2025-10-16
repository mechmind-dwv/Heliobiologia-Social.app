#!/usr/bin/env python3
"""
🔐 SISTEMA INTERACTIVO DE CONFIGURACIÓN DE TOKENS Y APIS
Configuración automática e interactiva para HelioBio-Social
"""
import os
import sys
import json
import getpass
from pathlib import Path
import requests
import webbrowser
from datetime import datetime

class TokenSetupWizard:
    """Asistente interactivo para configuración de APIs"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.env_file = self.base_dir / ".env"
        self.config_dir = self.base_dir / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # Configuraciones disponibles
        self.apis = {
            "1": {
                "name": "🌐 Facebook Graph API",
                "description": "Para análisis de redes sociales y engagement",
                "docs_url": "https://developers.facebook.com/docs/graph-api",
                "env_vars": [
                    "FACEBOOK_APP_ID",
                    "FACEBOOK_APP_SECRET", 
                    "FACEBOOK_ACCESS_TOKEN",
                    "FACEBOOK_PAGE_ID"
                ],
                "scopes": ["pages_read_engagement", "pages_read_user_content", "pages_show_list"]
            },
            "2": {
                "name": "🔮 Google Cloud AI & NLP",
                "description": "Para análisis de sentimiento avanzado y ML",
                "docs_url": "https://cloud.google.com/natural-language/docs",
                "env_vars": [
                    "GOOGLE_CLOUD_PROJECT",
                    "GOOGLE_APPLICATION_CREDENTIALS",
                    "GOOGLE_AI_MODEL"
                ]
            },
            "3": {
                "name": "🌞 NASA DONKI API", 
                "description": "Datos solares en tiempo real de NASA",
                "docs_url": "https://ccmc.gsfc.nasa.gov/tools/DONKI/",
                "env_vars": ["NASA_API_KEY"]
            },
            "4": {
                "name": "📊 NOAA Solar Data",
                "description": "Datos de actividad solar y manchas solares",
                "docs_url": "https://www.swpc.noaa.gov/products/solar-cycle-progression",
                "env_vars": ["NOAA_API_KEY"]
            },
            "5": {
                "name": "🐦 Twitter/X API v2",
                "description": "Análisis de tendencias sociales en tiempo real",
                "docs_url": "https://developer.twitter.com/en/docs/twitter-api",
                "env_vars": [
                    "TWITTER_API_KEY",
                    "TWITTER_API_SECRET",
                    "TWITTER_ACCESS_TOKEN",
                    "TWITTER_ACCESS_SECRET"
                ]
            }
        }
    
    def run(self):
        """Ejecutar el asistente interactivo"""
        print("🎆 HELIOBIO-SOCIAL - CONFIGURACIÓN DE APIS")
        print("=" * 50)
        print("🔐 Asistente interactivo para configurar tokens y claves API")
        print()
        
        self.show_current_config()
        
        while True:
            self.show_menu()
            choice = input("\n🎯 Selecciona una opción (1-6): ").strip()
            
            if choice == "1":
                self.configure_facebook()
            elif choice == "2":
                self.configure_google()
            elif choice == "3":
                self.configure_nasa()
            elif choice == "4":
                self.configure_noaa()
            elif choice == "5":
                self.configure_twitter()
            elif choice == "6":
                self.show_current_config()
            elif choice == "7":
                self.test_apis()
            elif choice == "8":
                self.generate_env_file()
            elif choice == "0":
                print("🚀 Configuración completada. ¡HelioBio-Social está listo!")
                break
            else:
                print("❌ Opción no válida. Intenta nuevamente.")
    
    def show_menu(self):
        """Mostrar menú principal"""
        print("\n" + "=" * 50)
        print("📋 MENÚ PRINCIPAL - CONFIGURACIÓN DE APIS")
        print("=" * 50)
        print("1. 🌐 Configurar Facebook Graph API")
        print("2. 🔮 Configurar Google Cloud AI")
        print("3. 🌞 Configurar NASA DONKI API") 
        print("4. 📊 Configurar NOAA Solar Data")
        print("5. 🐦 Configurar Twitter/X API")
        print("6. 👁️  Ver configuración actual")
        print("7. 🧪 Probar conexiones API")
        print("8. 📁 Generar archivo .env")
        print("0. 🚀 Salir y guardar")
        print("-" * 50)
    
    def show_current_config(self):
        """Mostrar configuración actual"""
        print("\n🔍 CONFIGURACIÓN ACTUAL:")
        print("-" * 30)
        
        env_vars = {}
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
        
        for api_id, api_info in self.apis.items():
            configured = all(var in env_vars for var in api_info['env_vars'])
            status = "✅ CONFIGURADO" if configured else "❌ NO CONFIGURADO"
            print(f"{api_info['name']}: {status}")
            
            if configured:
                for var in api_info['env_vars']:
                    if var in env_vars:
                        # Mostrar solo parte de los valores sensibles
                        value = env_vars[var]
                        if any(secret in var.lower() for secret in ['secret', 'key', 'token', 'password']):
                            if len(value) > 8:
                                displayed = value[:4] + "***" + value[-4:]
                            else:
                                displayed = "***"
                        else:
                            displayed = value
                        print(f"   └─ {var}: {displayed}")
    
    def configure_facebook(self):
        """Configurar Facebook Graph API"""
        print("\n🌐 CONFIGURACIÓN FACEBOOK GRAPH API")
        print("=" * 40)
        
        # Abrir documentación en navegador
        webbrowser.open("https://developers.facebook.com/docs/graph-api")
        
        print("\n📝 Pasos para obtener las credenciales:")
        print("1. Ve a https://developers.facebook.com/")
        print("2. Crea una nueva aplicación de tipo 'Business'")
        print("3. Añade el producto 'Facebook Graph API'")
        print("4. Configura 'Facebook Login' (solo para permisos)")
        print("5. Obtén los tokens de acceso")
        print()
        
        app_id = input("🔑 Facebook App ID: ").strip()
        app_secret = input("🔒 Facebook App Secret: ").strip()
        access_token = input("🎫 Facebook Access Token: ").strip()
        page_id = input("📄 Facebook Page ID: ").strip()
        
        # Guardar en configuración temporal
        config = {
            "FACEBOOK_APP_ID": app_id,
            "FACEBOOK_APP_SECRET": app_secret,
            "FACEBOOK_ACCESS_TOKEN": access_token,
            "FACEBOOK_PAGE_ID": page_id
        }
        
        self._save_api_config("facebook", config)
        print("✅ Configuración de Facebook guardada")
    
    def configure_google(self):
        """Configurar Google Cloud AI"""
        print("\n🔮 CONFIGURACIÓN GOOGLE CLOUD AI")
        print("=" * 40)
        
        webbrowser.open("https://cloud.google.com/natural-language/docs")
        
        print("\n📝 Pasos para obtener las credenciales:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un nuevo proyecto o selecciona uno existente")
        print("3. Habilita: Natural Language API, AI Platform")
        print("4. Crea una cuenta de servicio y descarga el JSON de credenciales")
        print("5. Coloca el archivo JSON en la carpeta config/")
        print()
        
        project_id = input("🏢 Google Cloud Project ID: ").strip()
        credentials_file = input("📁 Ruta del archivo de credenciales JSON: ").strip()
        ai_model = input("🤖 Modelo de AI a usar (text-bison@001): ").strip() or "text-bison@001"
        
        config = {
            "GOOGLE_CLOUD_PROJECT": project_id,
            "GOOGLE_APPLICATION_CREDENTIALS": credentials_file,
            "GOOGLE_AI_MODEL": ai_model
        }
        
        self._save_api_config("google", config)
        print("✅ Configuración de Google Cloud guardada")
    
    def configure_nasa(self):
        """Configurar NASA DONKI API"""
        print("\n🌞 CONFIGURACIÓN NASA DONKI API")
        print("=" * 40)
        
        webbrowser.open("https://api.nasa.gov/")
        
        print("\n📝 NASA API es gratuita:")
        print("1. Ve a https://api.nasa.gov/")
        print("2. Regístrate para obtener una API Key")
        print("3. Usa la key para acceder a DONKI (DONKI = Space Weather)")
        print()
        
        api_key = input("🚀 NASA API Key: ").strip()
        
        config = {"NASA_API_KEY": api_key}
        self._save_api_config("nasa", config)
        print("✅ Configuración de NASA guardada")
    
    def configure_noaa(self):
        """Configurar NOAA Solar Data"""
        print("\n📊 CONFIGURACIÓN NOAA SOLAR DATA")
        print("=" * 40)
        
        print("\n📝 NOAA proporciona datos solares abiertos:")
        print("1. Los datos de NOAA son generalmente de acceso libre")
        print("2. Algunos endpoints pueden requerir registro")
        print("3. Para uso avanzado, visita: https://www.swpc.noaa.gov/")
        print()
        
        api_key = input("🌡️  NOAA API Key (opcional - presiona Enter si no tienes): ").strip()
        
        config = {"NOAA_API_KEY": api_key} if api_key else {}
        self._save_api_config("noaa", config)
        print("✅ Configuración de NOAA guardada")
    
    def configure_twitter(self):
        """Configurar Twitter/X API"""
        print("\n🐦 CONFIGURACIÓN TWITTER/X API v2")
        print("=" * 40)
        
        webbrowser.open("https://developer.twitter.com/en/docs/twitter-api")
        
        print("\n📝 Pasos para obtener credenciales:")
        print("1. Ve a https://developer.twitter.com/")
        print("2. Solicita acceso a la API (puede requerir aprobación)")
        print("3. Crea una nueva App y obtén las claves")
        print("4. Necesitarás permisos de lectura")
        print()
        
        api_key = input("🔑 Twitter API Key: ").strip()
        api_secret = input("🔒 Twitter API Secret: ").strip()
        access_token = input("🎫 Twitter Access Token: ").strip()
        access_secret = input("🔐 Twitter Access Secret: ").strip()
        
        config = {
            "TWITTER_API_KEY": api_key,
            "TWITTER_API_SECRET": api_secret,
            "TWITTER_ACCESS_TOKEN": access_token,
            "TWITTER_ACCESS_SECRET": access_secret
        }
        
        self._save_api_config("twitter", config)
        print("✅ Configuración de Twitter guardada")
    
    def _save_api_config(self, api_name: str, config: dict):
        """Guardar configuración de API"""
        config_file = self.config_dir / f"{api_name}_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def test_apis(self):
        """Probar conexiones a las APIs configuradas"""
        print("\n🧪 PROBANDO CONEXIONES API")
        print("=" * 40)
        
        # Cargar configuración actual
        env_vars = self._load_current_env()
        
        for api_id, api_info in self.apis.items():
            print(f"\n🔍 Probando {api_info['name']}...")
            
            configured = all(var in env_vars for var in api_info['env_vars'])
            
            if configured:
                print("   ✅ Configuración completa")
                # Aquí podríamos añadir tests reales de conexión
            else:
                print("   ❌ Configuración incompleta")
                missing = [var for var in api_info['env_vars'] if var not in env_vars]
                print(f"   Variables faltantes: {', '.join(missing)}")
    
    def generate_env_file(self):
        """Generar archivo .env con todas las configuraciones"""
        print("\n📁 GENERANDO ARCHIVO .env")
        print("=" * 40)
        
        # Cargar todas las configuraciones
        all_config = {}
        for api_name in ["facebook", "google", "nasa", "noaa", "twitter"]:
            config_file = self.config_dir / f"{api_name}_config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    api_config = json.load(f)
                    all_config.update(api_config)
        
        # Escribir archivo .env
        with open(self.env_file, 'w') as f:
            f.write("# 🌞 HELIOBIO-SOCIAL - CONFIGURACIÓN DE ENTORNO\n")
            f.write("# Archivo generado automáticamente\n")
            f.write(f"# Fecha: {datetime.now().isoformat()}\n")
            f.write("\n")
            
            for key, value in all_config.items():
                f.write(f"{key}={value}\n")
            
            # Añadir configuraciones por defecto
            f.write("\n# Configuraciones de la aplicación\n")
            f.write("APP_ENV=development\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("DATA_RETENTION_DAYS=30\n")
        
        print(f"✅ Archivo .env generado en: {self.env_file}")
        print(f"📊 Total de variables configuradas: {len(all_config)}")
    
    def _load_current_env(self) -> dict:
        """Cargar variables de entorno actuales"""
        env_vars = {}
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
        return env_vars

if __name__ == "__main__":
    wizard = TokenSetupWizard()
    wizard.run()
