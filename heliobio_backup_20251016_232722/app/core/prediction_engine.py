"""
🧠 MOTOR DE PREDICCIÓN HELIOBIOLÓGICA COMPLETA v1.1
Sistema de Machine Learning con scikit-learn - VERSIÓN CORREGIDA
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional, Tuple
import pickle
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class AdvancedHelioBioPredictor:
    """Motor de predicción avanzado para resonancia solar-social - VERSIÓN CORREGIDA"""
    
    def __init__(self, model_path: str = "data/models/"):
        self.model_path = model_path
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        self.is_trained = False
        self.performance_metrics = {}
        self.training_history = []
        
        # Crear directorio de modelos si no existe
        os.makedirs(model_path, exist_ok=True)
    
    def load_models(self):
        """Cargar modelos avanzados pre-entrenados - MÉTODO AÑADIDO"""
        try:
            # Cargar scaler
            scaler_path = os.path.join(self.model_path, "advanced_scaler.pkl")
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scalers['advanced'] = pickle.load(f)
            
            # Cargar modelos
            model_files = {
                'random_forest_advanced': 'advanced_random_forest_advanced.pkl',
                'gradient_boosting': 'advanced_gradient_boosting.pkl',
                'poly_ridge': 'advanced_poly_ridge.pkl'
            }
            
            for name, filename in model_files.items():
                model_path = os.path.join(self.model_path, filename)
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        self.models[name] = pickle.load(f)
            
            # Cargar información
            info_path = os.path.join(self.model_path, "advanced_training_info.json")
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    info = json.load(f)
                    self.performance_metrics = info.get('performance_metrics', {})
                    self.feature_names = info.get('feature_names', [])
            
            self.is_trained = len(self.models) > 0
            logger.info(f"✅ Modelos avanzados cargados - Total: {len(self.models)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando modelos avanzados: {e}")
            self.is_trained = False

    def prepare_advanced_features(self, historical_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Preparar características avanzadas con ingeniería de features"""
        if len(historical_data) < 20:
            raise ValueError("Se necesitan al menos 20 puntos para entrenamiento avanzado")
        
        features = []
        targets = []
        feature_names = []
        
        # Usar ventana deslizante para características temporales
        window_size = 5
        
        for i in range(window_size, len(historical_data) - 1):
            window = historical_data[i-window_size:i]
            current = historical_data[i]
            next_point = historical_data[i + 1]
            
            # Características solares avanzadas
            sunspots_window = [p['solar'].get('sunspot_number', 0) for p in window]
            flares_window = [p['solar'].get('flare_activity', 0) for p in window]
            geomag_window = [p['solar'].get('geomagnetic_storm', 0) for p in window]
            
            solar_features = [
                np.mean(sunspots_window),  # Promedio
                np.std(sunspots_window),   # Volatilidad
                np.max(sunspots_window),   # Máximo
                np.min(sunspots_window),   # Mínimo
                sunspots_window[-1] - sunspots_window[0],  # Tendencia
                np.mean(flares_window),
                np.mean(geomag_window),
                current['solar'].get('solar_wind_speed', 0),
                current['solar'].get('coronal_holes', 0)
            ]
            
            # Características sociales avanzadas
            engagement_window = [p['social'].get('engagement_intensity', 0) for p in window]
            sentiment_window = [p['social'].get('sentiment_polarity', 0) for p in window]
            conflict_window = [p['social'].get('conflict_metric', 0) for p in window]
            
            social_features = [
                np.mean(engagement_window),
                np.std(engagement_window),
                np.mean(sentiment_window),
                np.std(sentiment_window),
                np.mean(conflict_window),
                current['social'].get('viral_content', 0),
                len(current['social'].get('trending_topics', [])),
                # Análisis de sentimiento de trending topics
                np.mean([t.get('sentiment', 0) for t in current['social'].get('trending_topics', [])]) if current['social'].get('trending_topics') else 0
            ]
            
            # Características de resonancia histórica
            resonance_window = [p['resonance'] for p in window]
            resonance_features = [
                np.mean(resonance_window),
                np.std(resonance_window),
                resonance_window[-1] - resonance_window[0],  # Tendencia
                current['resonance']
            ]
            
            # Características temporales cíclicas
            timestamp = datetime.fromisoformat(current['timestamp'])
            temporal_features = [
                timestamp.hour,
                timestamp.minute,
                timestamp.weekday(),
                timestamp.day / 31.0,  # Día del mes normalizado
                timestamp.month / 12.0  # Mes normalizado
            ]
            
            # Características de interacción solar-social
            interaction_features = [
                solar_features[0] * social_features[0] / 100,  # Sunspots × Engagement
                solar_features[1] * social_features[1] * 10,   # Volatilidad solar × volatilidad social
                resonance_features[0] * temporal_features[0] / 24  # Resonancia × hora del día
            ]
            
            # Combinar todas las características
            feature_vector = (solar_features + social_features + 
                            resonance_features + temporal_features + 
                            interaction_features)
            
            features.append(feature_vector)
            targets.append(next_point['resonance'])
        
        # Nombres de características para debugging
        feature_names = (
            [f'solar_mean', f'solar_std', f'solar_max', f'solar_min', f'solar_trend',
             f'flares_mean', f'geomag_mean', f'wind_speed', f'coronal_holes'] +
            [f'eng_mean', f'eng_std', f'sent_mean', f'sent_std', f'conflict_mean',
             f'viral_content', f'trending_count', f'trending_sentiment'] +
            [f'res_mean', f'res_std', f'res_trend', f'res_current'] +
            [f'hour', f'minute', f'weekday', f'day_norm', f'month_norm'] +
            [f'interaction_1', f'interaction_2', f'interaction_3']
        )
        
        return np.array(features), np.array(targets), feature_names
    
    def train_advanced_models(self, historical_data: List[Dict]) -> Dict:
        """Entrenar múltiples modelos avanzados de ML"""
        logger.info("🔮 Entrenando modelos avanzados de predicción heliobiológica...")
        
        try:
            # Preparar datos avanzados
            X, y, feature_names = self.prepare_advanced_features(historical_data)
            self.feature_names = feature_names
            
            if len(X) < 15:
                logger.warning("Datos insuficientes para entrenamiento avanzado")
                return {"error": "Datos insuficientes", "samples": len(X)}
            
            # Usar TimeSeriesSplit para validación temporal
            tscv = TimeSeriesSplit(n_splits=min(5, len(X) // 10))
            
            # Dividir datos manteniendo orden temporal
            split_point = int(0.8 * len(X))
            X_train, X_test = X[:split_point], X[split_point:]
            y_train, y_test = y[:split_point], y[split_point:]
            
            # Escalar características
            self.scalers['advanced'] = StandardScaler()
            X_train_scaled = self.scalers['advanced'].fit_transform(X_train)
            X_test_scaled = self.scalers['advanced'].transform(X_test)
            
            # Modelo 1: Random Forest avanzado
            self.models['random_forest_advanced'] = RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            self.models['random_forest_advanced'].fit(X_train_scaled, y_train)
            
            # Modelo 2: Gradient Boosting
            self.models['gradient_boosting'] = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            self.models['gradient_boosting'].fit(X_train_scaled, y_train)
            
            # Modelo 3: Ridge Regression con características polinómicas
            poly_ridge_pipeline = Pipeline([
                ('poly', PolynomialFeatures(degree=2, include_bias=False)),
                ('ridge', Ridge(alpha=1.0))
            ])
            self.models['poly_ridge'] = poly_ridge_pipeline
            self.models['poly_ridge'].fit(X_train_scaled, y_train)
            
            # Evaluar modelos con múltiples métricas
            self.performance_metrics = self._evaluate_advanced_models(X_test_scaled, y_test)
            
            # Guardar modelos e información de entrenamiento
            self._save_advanced_models()
            self._save_training_info(X_train.shape[0], X_test.shape[0])
            
            self.is_trained = True
            
            best_r2 = self.performance_metrics.get('best_r2', 0)
            logger.info(f"✅ Modelos avanzados entrenados - Mejor R²: {best_r2:.3f}")
            
            return self.performance_metrics
            
        except Exception as e:
            logger.error(f"❌ Error entrenando modelos avanzados: {e}")
            return {"error": str(e)}
    
    def _evaluate_advanced_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluación avanzada de modelos"""
        metrics = {}
        best_r2 = -1
        best_model = None
        
        for name, model in self.models.items():
            try:
                y_pred = model.predict(X_test)
                
                metrics[f'{name}_r2'] = r2_score(y_test, y_pred)
                metrics[f'{name}_mae'] = mean_absolute_error(y_test, y_pred)
                metrics[f'{name}_rmse'] = np.sqrt(mean_squared_error(y_test, y_pred))
                metrics[f'{name}_predictions'] = y_pred.tolist()
                
                # Actualizar mejor modelo
                if metrics[f'{name}_r2'] > best_r2:
                    best_r2 = metrics[f'{name}_r2']
                    best_model = name
                    
            except Exception as e:
                logger.error(f"Error evaluando modelo {name}: {e}")
                metrics[f'{name}_error'] = str(e)
        
        metrics['best_r2'] = best_r2
        metrics['best_model'] = best_model
        metrics['test_samples'] = len(X_test)
        
        return metrics
    
    def predict_advanced_resonance(self, current_data: Dict, historical_context: List[Dict], hours_ahead: int = 6) -> Dict:
        """Predicción avanzada usando contexto histórico"""
        if not self.is_trained:
            return {"error": "Modelos no entrenados", "advice": "Ejecutar /api/ml/train primero"}
        
        try:
            # Preparar características para predicción
            prediction_data = historical_context + [current_data]
            X_pred, _, _ = self.prepare_advanced_features(prediction_data)
            
            if len(X_pred) == 0:
                return {"error": "No se pudieron generar características para predicción"}
            
            # Usar el último punto para predicción
            X_current = X_pred[-1:]

            # Escalar características
            X_current_scaled = self.scalers['advanced'].transform(X_current)
            
            # Obtener predicciones de todos los modelos
            model_predictions = {}
            model_confidences = {}
            
            for name, model in self.models.items():
                try:
                    prediction = model.predict(X_current_scaled)[0]
                    model_predictions[name] = max(0.0, min(1.0, prediction))
                    model_confidences[name] = self.performance_metrics.get(f'{name}_r2', 0.5)
                except Exception as e:
                    logger.error(f"Error en predicción con {name}: {e}")
                    model_predictions[name] = current_data.get('resonance', 0.5)
                    model_confidences[name] = 0.3
            
            # Predicción ensemble (promedio ponderado por R²)
            total_confidence = sum(model_confidences.values())
            if total_confidence > 0:
                ensemble_prediction = sum(
                    pred * model_confidences[name] 
                    for name, pred in model_predictions.items()
                ) / total_confidence
            else:
                ensemble_prediction = sum(model_predictions.values()) / len(model_predictions)
            
            ensemble_prediction = max(0.0, min(1.0, ensemble_prediction))
            
            # Generar predicciones para múltiples horizontes con degradación temporal
            horizon_predictions = {}
            time_horizons = [1, 3, 6, 12, 24]
            
            for horizon in time_horizons:
                if horizon <= hours_ahead:
                    # Degradación más realista basada en volatilidad histórica
                    time_decay = 1.0 / (1 + 0.08 * horizon + 0.02 * horizon**2)
                    volatility = self.performance_metrics.get('best_r2', 0.7) * 0.3
                    
                    horizon_pred = ensemble_prediction * time_decay + volatility * (np.random.random() - 0.5)
                    horizon_predictions[f"{horizon}_hour"] = max(0.0, min(1.0, horizon_pred))
            
            # Análisis de importancia de características (si está disponible)
            feature_importance = {}
            if 'random_forest_advanced' in self.models:
                try:
                    importances = self.models['random_forest_advanced'].feature_importances_
                    top_indices = np.argsort(importances)[-5:][::-1]  # Top 5 características
                    for idx in top_indices:
                        if idx < len(self.feature_names):
                            feature_importance[self.feature_names[idx]] = float(importances[idx])
                except:
                    feature_importance = {"analysis": "no disponible"}
            
            return {
                "current_resonance": current_data.get('resonance', 0),
                "predicted_resonance": ensemble_prediction,
                "confidence": total_confidence / len(model_confidences),
                "model_predictions": model_predictions,
                "model_confidences": model_confidences,
                "best_model": self.performance_metrics.get('best_model', 'unknown'),
                "horizon_predictions": horizon_predictions,
                "feature_importance": feature_importance,
                "trend": "increasing" if ensemble_prediction > current_data.get('resonance', 0) else "decreasing",
                "trend_strength": abs(ensemble_prediction - current_data.get('resonance', 0)),
                "risk_level": self._calculate_advanced_risk(ensemble_prediction, current_data),
                "prediction_quality": self._assess_prediction_quality(ensemble_prediction),
                "timestamp": datetime.utcnow().isoformat(),
                "engine_version": "AdvancedML v1.1"
            }
            
        except Exception as e:
            logger.error(f"❌ Error en predicción avanzada: {e}")
            return {"error": str(e), "engine_version": "AdvancedML v1.1"}
    
    def _calculate_advanced_risk(self, prediction: float, current_data: Dict) -> str:
        """Cálculo avanzado de riesgo considerando múltiples factores"""
        base_risk = "HIGH" if prediction > 0.7 else "MODERATE" if prediction > 0.5 else "LOW"
        
        # Ajustar riesgo basado en volatilidad
        solar_volatility = current_data['solar'].get('flare_activity', 0) / 5.0
        social_volatility = current_data['social'].get('conflict_metric', 0)
        
        volatility_score = (solar_volatility + social_volatility) / 2
        
        if base_risk == "MODERATE" and volatility_score > 0.6:
            return "HIGH"
        elif base_risk == "LOW" and volatility_score > 0.7:
            return "MODERATE"
        
        return base_risk
    
    def _assess_prediction_quality(self, prediction: float) -> str:
        """Evaluar calidad de la predicción"""
        best_r2 = self.performance_metrics.get('best_r2', 0)
        
        if best_r2 > 0.8:
            return "EXCELLENT"
        elif best_r2 > 0.6:
            return "GOOD" 
        elif best_r2 > 0.4:
            return "FAIR"
        else:
            return "POOR"
    
    def _save_advanced_models(self):
        """Guardar modelos avanzados"""
        for name, model in self.models.items():
            model_path = os.path.join(self.model_path, f"advanced_{name}.pkl")
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
        
        # Guardar scaler
        scaler_path = os.path.join(self.model_path, "advanced_scaler.pkl")
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scalers['advanced'], f)
        
        # Guardar métricas y información
        advanced_info = {
            'performance_metrics': self.performance_metrics,
            'feature_names': self.feature_names,
            'training_date': datetime.utcnow().isoformat()
        }
        
        info_path = os.path.join(self.model_path, "advanced_training_info.json")
        with open(info_path, 'w') as f:
            json.dump(advanced_info, f, indent=2)
    
    def _save_training_info(self, train_samples: int, test_samples: int):
        """Guardar información del entrenamiento"""
        training_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'train_samples': train_samples,
            'test_samples': test_samples,
            'metrics': self.performance_metrics,
            'models_trained': list(self.models.keys())
        }
        
        self.training_history.append(training_record)
        
        # Mantener solo últimos 10 entrenamientos
        if len(self.training_history) > 10:
            self.training_history.pop(0)
    
    def get_advanced_model_info(self) -> Dict:
        """Obtener información detallada de los modelos avanzados"""
        return {
            "is_trained": self.is_trained,
            "models_loaded": list(self.models.keys()),
            "performance_metrics": self.performance_metrics,
            "feature_count": len(self.feature_names),
            "training_history_count": len(self.training_history),
            "best_model": self.performance_metrics.get('best_model', 'unknown'),
            "best_r2": self.performance_metrics.get('best_r2', 0),
            "engine_version": "AdvancedML v1.1"
        }

# Alias para compatibilidad
HelioBioPredictor = AdvancedHelioBioPredictor
