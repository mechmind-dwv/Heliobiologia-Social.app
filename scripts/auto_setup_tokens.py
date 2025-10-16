#!/usr/bin/env python3
"""
⚡ CONFIGURACIÓN AUTOMÁTICA DE TOKENS Y APIS
Script no interactivo para despliegues rápidos
"""
import os
import json
import argparse
from pathlib import Path

class AutoTokenSetup:
    """Configuración automática de APIs"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.env_file = self.base_dir / ".env"
        self.config_dir = self.base_dir / "config"
        self.config_dir.mkdir(exist_ok=True)
    
    def setup_from_args(self, args):
        """Configurar desde argumentos de línea de comandos"""
        configs = {}
        
        if args.facebook_app_id:
            configs.update({
                "FACEBOOK_APP_ID": args.facebook_app_id,
                "FACEBOOK_APP_SECRET": args.facebook_app_secret,
                "FACEBOOK_ACCESS_TOKEN": args.facebook_access_token,
                "FACEBOOK_PAGE_ID": args.facebook_page_id
            })
            self._save_api_config("facebook", {
                "FACEBOOK_APP_ID": args.facebook_app_id,
                "FACEBOOK_APP_SECRET": args.facebook_app_secret,
                "FACEBOOK_ACCESS_TOKEN": args.facebook_access_token,
                "FACEBOOK_PAGE_ID": args.facebook_page_id
            })
        
        if args.nasa_api_key:
            configs["NASA_API_KEY"] = args.nasa_api_key
            self._save_api_config("nasa", {"NASA_API_KEY": args.nasa_api_key})
        
        if args.noaa_api_key:
            configs["NOAA_API_KEY"] = args.noaa_api_key
            self._save_api_config("noaa", {"NOAA_API_KEY": args.noaa_api_key})
        
        if args.google_project:
            configs.update({
                "GOOGLE_CLOUD_PROJECT": args.google_project,
                "GOOGLE_APPLICATION_CREDENTIALS": args.google_credentials,
                "GOOGLE_AI_MODEL": args.google_model or "text-bison@001"
            })
            self._save_api_config("google", {
                "GOOGLE_CLOUD_PROJECT": args.google_project,
                "GOOGLE_APPLICATION_CREDENTIALS": args.google_credentials,
                "GOOGLE_AI_MODEL": args.google_model or "text-bison@001"
            })
        
        # Generar archivo .env
        self._generate_env_file(configs)
        
        print(f"✅ Configuración automática completada")
        print(f"📁 Archivo .env generado con {len(configs)} variables")
    
    def setup_from_env(self, env_file_path):
        """Configurar desde archivo .env existente"""
        if not os.path.exists(env_file_path):
            print(f"❌ Archivo {env_file_path} no encontrado")
            return
        
        # Copiar archivo .env
        import shutil
        shutil.copy(env_file_path, self.env_file)
        print(f"✅ Archivo .env copiado desde {env_file_path}")
    
    def _save_api_config(self, api_name: str, config: dict):
        """Guardar configuración de API"""
        config_file = self.config_dir / f"{api_name}_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _generate_env_file(self, configs: dict):
        """Generar archivo .env"""
        with open(self.env_file, 'w') as f:
            f.write("# 🌞 HELIOBIO-SOCIAL - CONFIGURACIÓN AUTOMÁTICA\n")
            f.write("# Generado por auto_setup_tokens.py\n\n")
            
            for key, value in configs.items():
                f.write(f"{key}={value}\n")
            
            # Configuraciones por defecto
            f.write("\n# Configuraciones por defecto\n")
            f.write("APP_ENV=production\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("DATA_RETENTION_DAYS=30\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configuración automática de APIs para HelioBio-Social")
    
    # Facebook arguments
    parser.add_argument('--facebook-app-id', help='Facebook App ID')
    parser.add_argument('--facebook-app-secret', help='Facebook App Secret')
    parser.add_argument('--facebook-access-token', help='Facebook Access Token')
    parser.add_argument('--facebook-page-id', help='Facebook Page ID')
    
    # NASA arguments
    parser.add_argument('--nasa-api-key', help='NASA API Key')
    
    # NOAA arguments  
    parser.add_argument('--noaa-api-key', help='NOAA API Key')
    
    # Google arguments
    parser.add_argument('--google-project', help='Google Cloud Project ID')
    parser.add_argument('--google-credentials', help='Google Credentials JSON path')
    parser.add_argument('--google-model', help='Google AI Model')
    
    # Environment file
    parser.add_argument('--from-env-file', help='Cargar configuración desde archivo .env')
    
    args = parser.parse_args()
    
    setup = AutoTokenSetup()
    
    if args.from_env_file:
        setup.setup_from_env(args.from_env_file)
    else:
        setup.setup_from_args(args)
