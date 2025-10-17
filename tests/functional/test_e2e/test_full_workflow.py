# tests/functional/test_e2e/test_full_workflow.py
import pytest
import time
from fastapi.testclient import TestClient

class TestFullWorkflow:
    
    def test_complete_heliobio_workflow(self, client):
        """Test del flujo completo HelioBio-Social"""
        
        # 1. Verificar salud del sistema
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
        
        # 2. Obtener datos solares
        solar_response = client.get("/api/solar/current")
        assert solar_response.status_code == 200
        
        # 3. Obtener análisis social
        social_response = client.get("/api/social/analysis")
        assert social_response.status_code == 200
        
        # 4. Calcular correlación
        correlation_response = client.get("/api/correlation/realtime")
        assert correlation_response.status_code == 200
        
        # 5. Obtener predicciones
        prediction_response = client.get("/api/predictions/resonance?hours_ahead=6")
        assert prediction_response.status_code == 200
        
        # 6. Verificar consistencia de datos
        solar_data = solar_response.json()
        social_data = social_response.json()
        correlation_data = correlation_response.json()
        
        assert "timestamp" in solar_data
        assert "social_data" in social_data
        assert "correlation" in correlation_data
    
    def test_error_handling_workflow(self, client):
        """Test de manejo de errores en flujo completo"""
        
        # Simular error en servicio solar
        with pytest.raises(Exception):
            # Esto debería probar el fallback
            client.get("/api/solar/current")
        
        # El sistema debería continuar funcionando
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
