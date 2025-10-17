# tests/unit/test_core/test_chizhevsky_engine.py
import pytest
from app.core.chizhevsky_engine import ChizhevskyEngine

class TestChizhevskyEngine:
    
    def test_calculate_resonance_index(self):
        """Test cálculo del índice de resonancia Chizhevsky"""
        engine = ChizhevskyEngine()
        
        solar_activity = 0.8
        social_tension = 0.6
        
        resonance = engine.calculate_resonance_index(
            solar_activity, 
            social_tension
        )
        
        assert 0 <= resonance <= 1
        assert isinstance(resonance, float)
    
    def test_detect_critical_points(self):
        """Test detección de puntos críticos"""
        engine = ChizhevskyEngine()
        
        time_series = [0.1, 0.3, 0.7, 0.9, 0.8, 0.4]
        critical_points = engine.detect_critical_points(time_series)
        
        assert isinstance(critical_points, list)
        assert len(critical_points) <= len(time_series)
    
    def test_historical_correlation(self):
        """Test cálculo de correlación histórica"""
        engine = ChizhevskyEngine()
        
        solar_data = [1, 2, 3, 4, 5]
        social_data = [2, 4, 6, 8, 10]
        
        correlation = engine.calculate_historical_correlation(
            solar_data, 
            social_data
        )
        
        assert -1 <= correlation <= 1
