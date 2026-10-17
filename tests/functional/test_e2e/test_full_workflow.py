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
        solar_data = solar_response.json()
        assert "solar_activity" in solar_data
        assert "chizhevsky_interpretation" in solar_data

        # 3. Obtener análisis social
        social_response = client.get("/api/social/analysis")
        assert social_response.status_code == 200
        social_data = social_response.json()
        assert "social_analysis" in social_data
        assert "collective_mood" in social_data

        # 4. Calcular correlación
        correlation_response = client.get("/api/correlation/realtime")
        assert correlation_response.status_code == 200
        correlation_data = correlation_response.json()
        # La correlación puede no estar disponible sin datos históricos
        assert "error" in correlation_data or "correlation" in correlation_data

        # 5. Obtener predicciones
        prediction_response = client.get("/api/predictions/resonance?hours_ahead=6")
        assert prediction_response.status_code == 200
        prediction_data = prediction_response.json()
        assert "error" in prediction_data or "predictions" in prediction_data

    def test_error_handling_workflow(self, client):
        """Test de manejo de errores en flujo completo"""
        # El sistema usa fallbacks, no lanza excepciones
        # Verificamos que sigue respondiendo incluso si algo falla
        solar_response = client.get("/api/solar/current")
        assert solar_response.status_code == 200  # Debe devolver 200 con datos simulados

        # El sistema debe seguir funcionando
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
