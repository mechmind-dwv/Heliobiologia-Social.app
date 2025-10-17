# tests/unit/test_services/test_nasa_service.py
import pytest
from unittest.mock import patch, Mock
from app.services.real_nasa_service import NASASolarService

class TestNASASolarService:
    
    @patch('app.services.real_nasa_service.requests.get')
    def test_fetch_solar_data_success(self, mock_get):
        """Test exitoso de obtención de datos solares"""
        # Mock de respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "flrID": "2024-01-01T12:00:00-FLR-001",
                "beginTime": "2024-01-01T12:00:00Z",
                "classType": "M5.2"
            }
        ]
        mock_get.return_value = mock_response
        
        service = NASASolarService()
        data = service.get_solar_flares()
        
        assert data is not None
        assert len(data) > 0
        assert 'flrID' in data[0]
    
    @patch('app.services.real_nasa_service.requests.get')
    def test_fetch_solar_data_failure(self, mock_get):
        """Test de fallo en obtención de datos"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        service = NASASolarService()
        data = service.get_solar_flares()
        
        # Debería retornar datos vacíos o de fallback
        assert data is not None
    
    def test_parse_solar_data(self):
        """Test parsing de datos solares"""
        service = NASASolarService()
        
        raw_data = [{"classType": "X1.5", "beginTime": "2024-01-01T12:00:00Z"}]
        parsed = service._parse_solar_data(raw_data)
        
        assert 'intensity' in parsed
        assert 'timestamp' in parsed
        assert parsed['intensity'] > 0
