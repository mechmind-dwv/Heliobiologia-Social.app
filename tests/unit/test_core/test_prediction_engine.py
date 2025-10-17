# tests/unit/test_core/test_prediction_engine.py
import pytest
import numpy as np
from unittest.mock import Mock, patch
from app.core.prediction_engine import PredictionEngine

class TestPredictionEngine:
    
    def test_engine_initialization(self):
        """Test que el motor de predicciones se inicializa correctamente"""
        engine = PredictionEngine()
        assert engine is not None
        assert hasattr(engine, 'models')
        assert hasattr(engine, 'scaler')
    
    def test_prepare_features(self, sample_solar_data, sample_social_data):
        """Test preparación de características para ML"""
        engine = PredictionEngine()
        
        features = engine._prepare_features(
            solar_data=sample_solar_data,
            social_data=sample_social_data
        )
        
        assert isinstance(features, np.ndarray)
        assert features.shape[0] > 0
    
    @patch('app.core.prediction_engine.PredictionEngine._load_models')
    def test_prediction_with_mock_data(self, mock_load):
        """Test predicción con datos mock"""
        engine = PredictionEngine()
        
        # Mock del modelo
        mock_model = Mock()
        mock_model.predict.return_value = np.array([0.75])
        engine.models = {'test_model': mock_model}
        
        prediction = engine.predict_resonance(
            solar_data=sample_solar_data,
            social_data=sample_social_data
        )
        
        assert 'test_model' in prediction
        assert prediction['test_model'] == 0.75
    
    def test_error_handling_invalid_data(self):
        """Test manejo de errores con datos inválidos"""
        engine = PredictionEngine()
        
        with pytest.raises(ValueError):
            engine._prepare_features(None, None)
