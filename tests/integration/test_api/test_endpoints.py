# tests/integration/test_api/test_endpoints.py
import pytest
from fastapi.testclient import TestClient

class TestAPIEndpoints:
    
    def test_health_endpoint(self, client):
        """Test endpoint de salud"""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "components" in data
    
    def test_solar_current_endpoint(self, client):
        """Test endpoint de datos solares actuales"""
        response = client.get("/api/solar/current")
        
        assert response.status_code == 200
        data = response.json()
        assert "solar_data" in data
        assert "timestamp" in data
    
    def test_social_analysis_endpoint(self, client):
        """Test endpoint de análisis social"""
        response = client.get("/api/social/analysis")
        
        assert response.status_code == 200
        data = response.json()
        assert "social_data" in data
        assert "analysis" in data
    
    def test_correlation_endpoint(self, client):
        """Test endpoint de correlación"""
        response = client.get("/api/correlation/realtime")
        
        assert response.status_code == 200
        data = response.json()
        assert "correlation" in data
        assert "confidence" in data
    
    def test_prediction_endpoint(self, client):
        """Test endpoint de predicciones"""
        response = client.get("/api/predictions/resonance?hours_ahead=6")
        
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert "timeframe" in data
    
    def test_invalid_endpoint(self, client):
        """Test endpoint inválido"""
        response = client.get("/api/invalid")
        assert response.status_code == 404

class TestAPIAuthentication:
    
    def test_protected_endpoints_without_auth(self, client):
        """Test endpoints protegidos sin autenticación"""
        # Esto debería fallar si implementamos auth
        response = client.get("/api/admin/status")
        # Por ahora asumimos 404 o manejo específico
        assert response.status_code in [404, 401, 403]
