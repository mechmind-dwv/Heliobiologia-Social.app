"""
⚙️ Configuración del Sistema HelioBio-Social
Frecuencias y parámetros del sistema consciente
"""
import os
from typing import Dict, Any
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Configuración principal del sistema"""
    
    # Configuración de la aplicación
    app_name: str = "HelioBio-Social v1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Facebook API Configuration
    facebook_app_id: str = Field(..., env="FACEBOOK_APP_ID")
    facebook_app_secret: str = Field(..., env="FACEBOOK_APP_SECRET")
    facebook_access_token: str = Field(..., env="FACEBOOK_ACCESS_TOKEN")
    facebook_page_id: str = Field(..., env="FACEBOOK_PAGE_ID")
    
    # Google Cloud Configuration
    google_cloud_project: str = Field(..., env="GOOGLE_CLOUD_PROJECT")
    google_application_credentials: str = Field(..., env="GOOGLE_APPLICATION_CREDENTIALS")
    
    # Solar Data Sources
    noaa_api_base: str = Field(default="https://services.swpc.noaa.gov/json/", env="NOAA_API_BASE")
    nasa_api_key: str = Field(default="", env="NASA_API_KEY")
    silso_data_url: str = Field(default="http://www.sidc.be/silso/DATA/SN_d_tot_V2.0.csv", env="SILSO_DATA_URL")
    
    # Analysis Parameters
    correlation_methods: list = ["pearson", "spearman", "granger", "wavelet"]
    time_windows: Dict[str, int] = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "11_year_cycle": 4018  # días en 11 años
    }
    confidence_threshold: float = 0.05
    
    # Chizhevsky Parameters
    solar_max_amplification: float = 1.8
    geomagnetic_sensitivity: float = 0.7
    social_crispation_threshold: float = 0.65
    
    # Data Management
    data_retention_days: int = Field(default=365, env="DATA_RETENTION_DAYS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
_settings_instance = None

def get_settings() -> Settings:
    """Obtener instancia de configuración (singleton)"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance

def get_chizhevsky_parameters() -> Dict[str, Any]:
    """Obtener parámetros específicos del modelo Chizhevsky"""
    settings = get_settings()
    return {
        "solar_max_amplification": settings.solar_max_amplification,
        "geomagnetic_sensitivity": settings.geomagnetic_sensitivity,
        "social_crispation_threshold": settings.social_crispation_threshold,
        "time_windows": settings.time_windows
    }
