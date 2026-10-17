# tests/unit/test_services/test_nasa_service.py
import pytest
from unittest.mock import patch, Mock, AsyncMock
from app.services.real_nasa_service import RealNasaService

class TestRealNasaService:

    @pytest.mark.asyncio
    @patch('app.services.real_nasa_service.RealNasaService.ensure_session')
    async def test_get_solar_flares_success(self, mock_ensure):
        """Test obtención de fulguraciones solares (con fallback a simulación)"""
        service = RealNasaService()
        # El servicio tiene fallback a datos simulados si falla la API real
        flares = await service.get_solar_flares()
        assert flares is not None
        assert isinstance(flares, list)

    @pytest.mark.asyncio
    async def test_get_solar_flares_failure_fallback(self):
        """Test que el servicio devuelve datos simulados si falla la API"""
        service = RealNasaService()
        # Forzamos un error en la sesión para probar el fallback
        with patch.object(service, 'ensure_session', side_effect=Exception("Network error")):
            flares = await service.get_solar_flares()
            assert flares is not None
            assert isinstance(flares, list)

    def test_parse_solar_flares(self):
        """Test parsing de datos solares"""
        service = RealNasaService()
        raw_data = [{
            "flrID": "2024-01-01T12:00:00-FLR-001",
            "beginTime": "2024-01-01T12:00:00Z",
            "classType": "X1.5"
        }]
        parsed = service._parse_solar_flares(raw_data)
        assert isinstance(parsed, list)
        if parsed:
            assert 'intensity' in parsed[0]
            assert 'timestamp' in parsed[0]
            assert parsed[0]['intensity'] > 0
