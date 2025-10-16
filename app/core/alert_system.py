"""
🚨 SISTEMA DE ALERTAS INTELIGENTES HELIOBIO-SOCIAL
Alertas proactivas basadas en patrones críticos de resonancia
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class Alert:
    """Estructura de alerta del sistema"""
    level: str  # INFO, WARNING, CRITICAL
    type: str   # SOLAR, SOCIAL, RESONANCE, CRISPATION
    title: str
    message: str
    timestamp: datetime
    duration: timedelta
    data: Dict
    acknowledged: bool = False

class AlertSystem:
    """Sistema de alertas inteligentes para HelioBio-Social"""
    
    def __init__(self):
        self.active_alerts: List[Alert] = []
        self.alert_history: List[Alert] = []
        self.alert_cooldowns: Dict[str, datetime] = {}
        
        # Umbrales de alerta basados en investigación Chizhevsky
        self.thresholds = {
            'solar_storm_critical': 0.8,      # Resonancia > 80%
            'solar_activity_high': 0.7,       # Resonancia > 70%
            'social_crispation_high': 0.6,    # Conflicto > 60%
            'flare_activity_critical': 4,     # Fulguraciones nivel 4-5
            'geomagnetic_storm_severe': 3,    # Tormenta geomagnética severa
            'sunspots_extreme': 120,          # Manchas solares extremas
            'engagement_anomaly': 0.3,        # Cambio brusco en engagement
        }
    
    async def analyze_conditions(self, solar_data: Dict, social_data: Dict, resonance: float) -> List[Alert]:
        """Analizar condiciones actuales y generar alertas si es necesario"""
        new_alerts = []
        
        # Verificar condiciones solares críticas
        solar_alerts = await self._check_solar_conditions(solar_data, resonance)
        new_alerts.extend(solar_alerts)
        
        # Verificar condiciones sociales críticas
        social_alerts = await self._check_social_conditions(social_data, resonance)
        new_alerts.extend(social_alerts)
        
        # Verificar resonancia crítica
        resonance_alerts = await self._check_resonance_conditions(resonance, solar_data, social_data)
        new_alerts.extend(resonance_alerts)
        
        # Actualizar estado de alertas
        for alert in new_alerts:
            await self._add_alert(alert)
        
        return new_alerts
    
    async def _check_solar_conditions(self, solar_data: Dict, resonance: float) -> List[Alert]:
        """Verificar condiciones solares que requieren alerta"""
        alerts = []
        
        sunspots = solar_data.get('sunspot_number', 0)
        flare_activity = solar_data.get('flare_activity', 0)
        geomagnetic_storm = solar_data.get('geomagnetic_storm', 0)
        
        # Alerta: Actividad solar extrema
        if sunspots > self.thresholds['sunspots_extreme']:
            if self._can_trigger_alert('solar_extreme'):
                alerts.append(Alert(
                    level="CRITICAL",
                    type="SOLAR",
                    title="🌋 ACTIVIDAD SOLAR EXTREMA DETECTADA",
                    message=f"Manchas solares en nivel crítico ({sunspots}). Máxima influencia en psique colectiva esperada.",
                    timestamp=datetime.utcnow(),
                    duration=timedelta(hours=24),
                    data={'sunspots': sunspots, 'impact': 'high'}
                ))
        
        # Alerta: Fulguraciones intensas
        if flare_activity >= self.thresholds['flare_activity_critical']:
            if self._can_trigger_alert('flare_critical'):
                alerts.append(Alert(
                    level="CRITICAL", 
                    type="SOLAR",
                    title="⚡ FULGURACIONES SOLARES INTENSAS",
                    message=f"Actividad de fulguraciones nivel {flare_}/5. Posible impacto en sistemas de comunicación y comportamiento social.",
                    timestamp=datetime.utcnow(),
                    duration=timedelta(hours=12),
                    data={'flare_level': flare_activity, 'impact': 'medium'}
                ))
        
        # Alerta: Tormenta geomagnética severa
        if geomagnetic_storm >= self.thresholds['geomagnetic_storm_severe']:
            if self._can_trigger_alert('geomagnetic_severe'):
                alerts.append(Alert(
                    level="WARNING",
                    type="SOLAR",
                    title="🧲 TORMENTA GEOMAGNÉTICA ACTIVA",
                    message=f"Tormenta geomagnética nivel {geomagnetic_storm}/4. Afectación potencial en sistemas biológicos y estados de ánimo.",
                    timestamp=datetime.utcnow(),
                    duration=timedelta(hours=6),
                    data={'storm_level': geomagnetic_storm, 'impact': 'medium'}
                ))
        
        return alerts
    
    async def _check_social_conditions(self, social_data: Dict, resonance: float) -> List[Alert]:
        """Verificar condiciones sociales que requieren alerta"""
        alerts = []
        
        conflict_metric = social_data.get('conflict_metric', 0)
        engagement = social_data.get('engagement_intensity', 0)
        sentiment = social_data.get('sentiment_polarity', 0)
        
        # Alerta: Alta crispación social
        if conflict_metric > self.thresholds['social_crispation_high']:
            if self._can_trigger_alert('crispation_high'):
                alerts.append(Alert(
                    level="WARNING",
                    type="SOCIAL", 
                    title="🌪️ ALTA CRISPACIÓN SOCIAL DETECTADA",
                    message=f"Nivel de conflicto en {conflict_metric:.1%}. Condiciones propicias para eventos sociales significativos.",
                    timestamp=datetime.utcnow(),
                    duration=timedelta(hours=6),
                    data={'conflict_level': conflict_metric, 'sentiment': sentiment}
                ))
        
        # Alerta: Anomalía en engagement
        engagement_change = self._calculate_engagement_change()
        if abs(engagement_change) > self.thresholds['engagement_anomaly']:
            if self._can_trigger_alert('engagement_anomaly'):
                trend = "aumento" if engagement_change > 0 else "disminución"
                alerts.append(Alert(
                    level="INFO",
                    type="SOCIAL",
                    title="📊 ANOMALÍA EN PARTICIPACIÓN SOCIAL",
                    message=f"{trend.title()} brusco del engagement ({engagement_change:+.1%}). Posible evento viral o cambio de tendencia.",
                    timestamp=datetime.utcnow(), 
                    duration=timedelta(hours=2),
                    data={'engagement_change': engagement_change, 'current_engagement': engagement}
                ))
        
        return alerts
    
    async def _check_resonance_conditions(self, resonance: float, solar_data: Dict, social_data: Dict) -> List[Alert]:
        """Verificar condiciones de resonancia crítica"""
        alerts = []
        
        # Alerta: Resonancia crítica (condiciones Chizhevsky)
        if resonance > self.thresholds['solar_storm_critical']:
            if self._can_trigger_alert('resonance_critical'):
                alerts.append(Alert(
                    level="CRITICAL",
                    type="RESONANCE",
                    title="🎆 RESONANCIA SOLAR-SOCIAL CRÍTICA",
                    message="Condiciones similares a máximos solares históricos. Alta probabilidad de eventos sociales significativos según teoría de Chizhevsky.",
                    timestamp=datetime.utcnow(),
                    duration=timedelta(hours=48),
                    data={'resonance': resonance, 'chizhevsky_phase': 'maximum'}
                ))
        
        # Alerta: Resonancia alta
        elif resonance > self.thresholds['solar_activity_high']:
            if self._can_trigger_alert('resonance_high'):
                alerts.append(Alert(
                    level="WARNING", 
                    type="RESONANCE",
                    title="🔥 RESONANCIA SOLAR-SOCIAL ELEVADA",
                    message="Alta correlación detectada. Influencia solar significativa en comportamiento social esperada.",
                    timestamp=datetime.utcnow(),
                    duration=timedelta(hours=12),
                    data={'resonance': resonance, 'chizhevsky_phase': 'ascending'}
                ))
        
        return alerts
    
    def _can_trigger_alert(self, alert_type: str) -> bool:
        """Verificar si se puede disparar una alerta (evitar spam)"""
        now = datetime.utcnow()
        last_trigger = self.alert_cooldowns.get(alert_type)
        
        if last_trigger:
            # Cooldowns específicos por tipo de alerta
            cooldowns = {
                'solar_extreme': timedelta(hours=6),
                'flare_critical': timedelta(hours=3),
                'geomagnetic_severe': timedelta(hours=2),
                'crispation_high': timedelta(hours=4),
                'engagement_anomaly': timedelta(minutes=30),
                'resonance_critical': timedelta(hours=12),
                'resonance_high': timedelta(hours=6)
            }
            
            cooldown = cooldowns.get(alert_type, timedelta(hours=1))
            if now - last_trigger < cooldown:
                return False
        
        self.alert_cooldowns[alert_type] = now
        return True
    
    def _calculate_engagement_change(self) -> float:
        """Calcular cambio en engagement (simulado por ahora)"""
        # En implementación real, compararía con datos históricos
        import random
        return random.uniform(-0.4, 0.4)
    
    async def _add_alert(self, alert: Alert):
        """Añadir alerta al sistema"""
        self.active_alerts.append(alert)
        self.alert_history.append(alert)
        
        # Mantener máximo 100 alertas históricas
        if len(self.alert_history) > 100:
            self.alert_history.pop(0)
        
        # Log de alerta crítica
        if alert.level == "CRITICAL":
            logger.warning(f"🚨 ALERTA CRÍTICA: {alert.title}")
        elif alert.level == "WARNING":
            logger.info(f"⚠️ ALERTA: {alert.title}")
        else:
            logger.info(f"ℹ️ INFO: {alert.title}")
    
    async def get_active_alerts(self) -> List[Alert]:
        """Obtener alertas activas no expiradas"""
        now = datetime.utcnow()
        active = []
        
        for alert in self.active_alerts:
            if now - alert.timestamp < alert.duration and not alert.acknowledged:
                active.append(alert)
            else:
                alert.acknowledged = True
        
        # Limpiar alertas expiradas
        self.active_alerts = [a for a in self.active_alerts if not a.acknowledged]
        
        return active
    
    async def acknowledge_alert(self, alert_id: int):
        """Marcar alerta como reconocida"""
        if 0 <= alert_id < len(self.active_alerts):
            self.active_alerts[alert_id].acknowledged = True
    
    async def get_alert_stats(self) -> Dict:
        """Obtener estadísticas de alertas"""
        now = datetime.utcnow()
        last_24h = [a for a in self.alert_history if now - a.timestamp < timedelta(hours=24)]
        
        return {
            'active_alerts': len(self.active_alerts),
            'alerts_24h': len(last_24h),
            'critical_alerts': len([a for a in last_24h if a.level == 'CRITICAL']),
            'warning_alerts': len([a for a in last_24h if a.level == 'WARNING']),
            'solar_alerts': len([a for a in last_24h if a.type == 'SOLAR']),
            'social_alerts': len([a for a in last_24h if a.type == 'SOCIAL']),
        }
