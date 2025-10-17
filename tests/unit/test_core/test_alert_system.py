# tests/unit/test_core/test_alert_system.py
import pytest
from datetime import datetime
from app.core.alert_system import AlertSystem

class TestAlertSystem:
    
    def test_alert_creation(self):
        """Test creación de alertas"""
        alert_system = AlertSystem()
        
        alert = alert_system.create_alert(
            level="HIGH",
            message="Test alert",
            source="TEST_SYSTEM"
        )
        
        assert alert['level'] == "HIGH"
        assert alert['message'] == "Test alert"
        assert 'timestamp' in alert
        assert alert['resolved'] is False
    
    def test_alert_thresholds(self):
        """Test evaluación de umbrales de alerta"""
        alert_system = AlertSystem()
        
        # Test umbral bajo
        assert not alert_system._check_threshold(0.3, "HIGH")
        
        # Test umbral alto
        assert alert_system._check_threshold(0.9, "HIGH")
    
    def test_alert_resolution(self):
        """Test resolución de alertas"""
        alert_system = AlertSystem()
        
        alert_id = alert_system.create_alert("MEDIUM", "Test")['id']
        result = alert_system.resolve_alert(alert_id)
        
        assert result is True
        assert alert_system.get_alert(alert_id)['resolved'] is True
