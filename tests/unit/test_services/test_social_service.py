# tests/unit/test_services/test_social_service.py
import pytest
from unittest.mock import patch, Mock
from app.services.hybrid_social_service import HybridSocialService

class TestHybridSocialService:
    
    @patch('app.services.hybrid_social_service.requests.get')
    def test_fetch_engagement_data(self, mock_get):
        """Test obtención de datos de engagement"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "engagement": {"rate": 0.045},
            "sentiment": {"score": 0.78}
        }
        mock_get.return_value = mock_response
        
        service = HybridSocialService()
        data = service.get_engagement_data()
        
        assert data is not None
        assert 'engagement' in data
        assert 'sentiment' in data
    
    def test_simulated_social_data(self):
        """Test generación de datos sociales simulados"""
        service = HybridSocialService()
        
        # Forzar modo simulado
        service.use_simulated_data = True
        data = service.get_engagement_data()
        
        assert data is not None
        assert 'engagement' in data
        assert 'sentiment' in data
        assert isinstance(data['engagement']['rate'], float)
    
    def test_calculate_social_tension(self):
        """Test cálculo de tensión social"""
        service = HybridSocialService()
        
        social_data = {
            'engagement': {'rate': 0.8},
            'sentiment': {'score': 0.2},
            'post_count': 1000
        }
        
        tension = service._calculate_social_tension(social_data)
        
        assert 0 <= tension <= 1
        assert isinstance(tension, float)
