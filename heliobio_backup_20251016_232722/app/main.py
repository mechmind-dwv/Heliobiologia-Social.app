"""
🌞 HELIOBIO-SOCIAL v1.5.0 - CON APIS REALES
Sistema con conexiones reales a Facebook, NASA y ML avanzado
"""
import asyncio
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import random

from app.services.real_solar_service import RealSolarService
from app.services.social_analyzer_service import SocialAnalyzerService
from app.core.alert_system import AlertSystem
from app.core.prediction_engine import HelioBioPredictor
from app.services.real_facebook_service import RealFacebookService
from app.services.real_nasa_service import RealNasaService

# Servicios globales
solar_service = RealSolarService()
social_service = SocialAnalyzerService()
facebook_service = RealFacebookService()
nasa_service = RealNasaService()
alert_system = AlertSystem()
predictor = HelioBioPredictor()
historical_data = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida del sistema con APIs reales"""
    global historical_data
    
    print("🎆 HELIOBIO-SOCIAL v1.5.0 - APIS REALES ACTIVADAS")
    print("🌐 Conectando con Facebook Graph API...")
    print("🌞 Conectando con NASA DONKI API...")
    print("🧠 Cargando modelos de predicción...")
    
    try:
        # Cargar modelos existentes
        predictor.load_models()
        
        # Inicializar servicios
        await update_system_data()
        asyncio.create_task(continuous_data_update())
        
        # Entrenar modelos si hay datos suficientes
        asyncio.create_task(train_models_periodically())
        
        print("✅ Sistema con APIs reales activado correctamente")
        yield
        
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        raise
    finally:
        print("🛑 Apagando sistema HelioBio-Social...")
        # Cerrar conexiones
        await facebook_service.close()
        await nasa_service.close()

async def update_system_data():
    """Actualizar todos los datos del sistema con APIs reales"""
    global historical_data
    
    try:
        # Obtener datos solares REALES de NASA
        solar_data = await nasa_service.get_current_solar_activity()
        
        # Obtener datos sociales REALES de Facebook
        social_data = await facebook_service.get_social_analysis()
        
        # Calcular resonancia
        resonance = calculate_resonance(solar_data, social_data)
        current_data = {
            'solar': solar_data,
            'social': social_data,
            'resonance': resonance
        }
        
        # Analizar condiciones para alertas
        new_alerts = await alert_system.analyze_conditions(solar_data, social_data, resonance)
        
        # Guardar histórico
        historical_data.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'solar': solar_data,
            'social': social_data,
            'resonance': resonance,
            'alerts_triggered': len(new_alerts)
        })
        
        # Mantener últimos 200 puntos para entrenamiento ML
        if len(historical_data) > 200:
            historical_data.pop(0)
            
    except Exception as e:
        print(f"❌ Error actualizando datos del sistema: {e}")
        # En caso de error, usar datos simulados como fallback
        solar_data = await solar_service.get_current_solar_data()
        social_data = await social_service.get_social_analysis()
        
        resonance = calculate_resonance(solar_data, social_data)
        historical_data.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'solar': solar_data,
            'social': social_data,
            'resonance': resonance,
            'alerts_triggered': 0
        })

async def continuous_data_update():
    """Actualización continua cada 60 segundos (más lento para APIs reales)"""
    while True:
        await update_system_data()
        await asyncio.sleep(60)

async def train_models_periodically():
    """Entrenar modelos ML periódicamente"""
    while True:
        await asyncio.sleep(1800)  # Cada 30 minutos
        
        if len(historical_data) >= 30:  # Mínimo para entrenar
            print("🔄 Re-entrenando modelos ML avanzados...")
            try:
                metrics = predictor.train_advanced_models(historical_data)
                if metrics and 'error' not in metrics:
                    best_r2 = metrics.get('best_r2', 0)
                    samples = metrics.get('test_samples', 0)
                    print(f"✅ Modelos actualizados - R²: {best_r2:.3f}, Muestras: {samples}")
                else:
                    print("⚠️  Modelos no pudieron ser entrenados (datos insuficientes)")
            except Exception as e:
                print(f"❌ Error entrenando modelos: {e}")

def calculate_resonance(solar, social):
    """Calcular resonancia mejorada"""
    solar_intensity = solar.get('sunspot_number', 0) / 150.0
    social_tension = social.get('engagement_intensity', 0) / 100.0
    flare_impact = solar.get('flare_activity', 0) / 5.0
    geomagnetic_impact = solar.get('geomagnetic_storm', 0) / 4.0
    
    resonance = (
        solar_intensity * 0.20 + 
        social_tension * 0.25 + 
        flare_impact * 0.25 +
        geomagnetic_impact * 0.30
    )
    return min(1.0, resonance)

# APP FASTAPI
app = FastAPI(
    title="HelioBio-Social API",
    description="Sistema de Análisis Heliobiológico con APIs Reales y ML",
    version="1.5.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def serve_dashboard():
    return FileResponse('app/static/dashboard.html')

@app.get("/api/health")
async def health_check():
    solar_data = historical_data[-1]['solar'] if historical_data else {}
    social_data = historical_data[-1]['social'] if historical_data else {}
    alert_stats = await alert_system.get_alert_stats()
    model_info = predictor.get_advanced_model_info()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "real-apis-1.5",
        "components": {
            "solar_monitor": solar_data.get('data_source', 'unknown'),
            "social_analyzer": social_data.get('data_source', 'unknown'),
            "facebook_api": "active" if hasattr(facebook_service, 'real_mode') and facebook_service.real_mode else "simulation",
            "nasa_api": "active" if hasattr(nasa_service, 'real_mode') and nasa_service.real_mode else "simulation",
            "alert_system": "active",
            "ml_predictor": "active" if model_info["is_trained"] else "training_required",
            "dashboard": "active"
        },
        "alert_stats": alert_stats,
        "ml_info": model_info
    }

@app.get("/api/solar/current")
async def get_current_solar_activity():
    solar_data = historical_data[-1]['solar'] if historical_data else await nasa_service.get_current_solar_activity()
    return {
        "solar_activity": solar_data,
        "chizhevsky_interpretation": get_solar_interpretation(solar_data),
        "data_source": solar_data.get('data_source', 'unknown')
    }

@app.get("/api/social/analysis")
async def get_social_analysis():
    social_data = historical_data[-1]['social'] if historical_data else await facebook_service.get_social_analysis()
    return {
        "social_analysis": social_data,
        "collective_mood": get_social_mood(social_data),
        "data_source": social_data.get('data_source', 'unknown')
    }

@app.get("/api/correlation/realtime")
async def get_realtime_correlation():
    if not historical_data:
        return {"error": "No data available"}
    
    solar_data = historical_data[-1]['solar']
    social_data = historical_data[-1]['social']
    resonance = historical_data[-1]['resonance']
    
    interpretation = "ALTA RESONANCIA" if resonance > 0.7 else "RESONANCIA MODERADA" if resonance > 0.4 else "RESONANCIA BAJA"
    
    return {
        "correlation_analysis": {
            "solar_social_resonance": round(resonance, 3),
            "interpretation": interpretation,
            "confidence": 0.85,
            "solar_cycle_phase": solar_data.get('solar_cycle_phase', 'unknown')
        },
        "crispation_alert": {
            "level": "HIGH" if resonance > 0.7 else "MODERATE" if resonance > 0.5 else "LOW",
            "message": get_alert_message(resonance)
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/predictions/resonance")
async def get_resonance_predictions(hours_ahead: int = 6):
    """Predicciones ML de resonancia"""
    if not historical_data:
        return {"error": "No hay datos históricos"}
    
    if not predictor.is_trained:
        return {"error": "Modelos ML no entrenados", "suggestion": "Esperar más datos históricos"}
    
    current_data = historical_data[-1]
    prediction = predictor.predict_advanced_resonance(current_data, historical_data, hours_ahead)
    
    return {
        "prediction_engine": "HelioBio-ML v1.1",
        "current_data": {
            "timestamp": current_data['timestamp'],
            "resonance": current_data['resonance']
        },
        "predictions": prediction,
        "model_info": predictor.get_advanced_model_info(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/ml/train")
async def train_ml_models():
    """Forzar entrenamiento de modelos ML"""
    if len(historical_data) < 20:
        raise HTTPException(status_code=400, detail="Se necesitan al menos 20 puntos de datos históricos")
    
    metrics = predictor.train_advanced_models(historical_data)
    
    if metrics and 'error' not in metrics:
        return {
            "status": "success",
            "message": f"Modelos entrenados - R²: {metrics.get('best_r2', 0):.3f}",
            "metrics": metrics,
            "training_samples": len(historical_data) - 1
        }
    else:
        raise HTTPException(status_code=500, detail="Error entrenando modelos")

@app.get("/api/alerts/active")
async def get_active_alerts():
    """Alertas activas del sistema"""
    active_alerts = await alert_system.get_active_alerts()
    
    return {
        "alerts": [
            {
                "id": i,
                "level": alert.level,
                "type": alert.type,
                "title": alert.title,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "duration_hours": alert.duration.total_seconds() / 3600,
                "data": alert.data
            }
            for i, alert in enumerate(active_alerts)
        ],
        "total_active": len(active_alerts),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/alerts/stats")
async def get_alert_stats():
    """Estadísticas de alertas"""
    return await alert_system.get_alert_stats()

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """Reconocer alerta"""
    await alert_system.acknowledge_alert(alert_id)
    return {"status": "alert acknowledged", "alert_id": alert_id}

@app.get("/api/historical/data")
async def get_historical_data(hours: int = 6):
    cutoff_time = datetime.now(timezone.utc).timestamp() - (hours * 3600)
    filtered_data = [
        point for point in historical_data 
        if datetime.fromisoformat(point['timestamp']).timestamp() > cutoff_time
    ]
    return {
        "time_range_hours": hours,
        "data_points": len(filtered_data),
        "data": filtered_data[-50:]
    }

@app.get("/api/social/trending")
async def get_trending_topics():
    """Temas trending actuales"""
    social_data = historical_data[-1]['social'] if historical_data else await social_service.get_social_analysis()
    return {
        "trending_topics": social_data.get('trending_topics', []),
        "dominant_emotion": social_data.get('dominant_emotion', 'unknown'),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/facebook/insights")
async def get_facebook_insights():
    """Insights detallados de Facebook"""
    insights = await facebook_service.get_page_insights()
    posts = await facebook_service.get_page_posts(5)
    
    return {
        "page_insights": insights,
        "recent_posts": posts,
        "data_source": insights.get('data_source', 'unknown'),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/nasa/flares")
async def get_nasa_flares():
    """Fulguraciones solares de NASA"""
    flares = await nasa_service.get_solar_flares()
    
    # Filtrar fulguraciones recientes (últimas 24 horas)
    now_utc = datetime.now(timezone.utc)
    recent_flares = [
        f for f in flares 
        if f.get('_begin_dt') and f['_begin_dt'] > now_utc - timedelta(hours=24)
    ]
    
    return {
        "solar_flares": flares,
        "total_flares": len(flares),
        "recent_flares": recent_flares,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Funciones de interpretación
def get_solar_interpretation(solar_data):
    sunspots = solar_data.get('sunspot_number', 0)
    flares = solar_data.get('flare_activity', 0)
    
    if sunspots > 100 and flares > 3:
        return "🌋 ACTIVIDAD SOLAR ELEVADA - Máxima influencia en psique colectiva"
    elif sunspots > 60:
        return "🔥 ACTIVIDAD MODERADA-ALTA - Influencia significativa detectada"
    elif sunspots > 30:
        return "⚡ ACTIVIDAD MODERADA - Influencia en tono emocional"
    else:
        return "🌊 ACTIVIDAD BAJA - Influencia solar mínima"

def get_social_mood(social_data):
    emotion = social_data.get('dominant_emotion', 'neutral')
    engagement = social_data.get('engagement_intensity', 0)
    
    if emotion == 'positive' and engagement > 70:
        return "🌟 ARMONÍA COLECTIVA - Estados positivos dominantes"
    elif emotion == 'negative' and engagement > 70:
        return "🌪️ CRISPACIÓN DETECTABLE - Tensión social elevada"
    elif engagement > 80:
        return "🔥 ALTA ACTIVIDAD - Participación intensa"
    elif emotion == 'positive':
        return "💫 ENERGÍA POSITIVA - Estados optimistas"
    else:
        return "🌊 ESTADO NEUTRO - Condiciones base estables"

def get_alert_message(resonance):
    if resonance > 0.7:
        return "🚨 ALTA RESONANCIA - Eventos sociales significativos probables"
    elif resonance > 0.5:
        return "📡 RESONANCIA MODERADA - Monitorizar tendencias"
    else:
        return "✅ CONDICIONES ESTABLES - Resonancia normal"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# Añadir import del servicio híbrido
from app.services.hybrid_social_service import hybrid_service

# Modificar la función update_system_data para usar el servicio híbrido
async def update_system_data():
    """Actualizar todos los datos del sistema con APIs reales y análisis híbrido"""
    global historical_data
    
    try:
        # Obtener datos solares REALES de NASA
        solar_data = await nasa_service.get_current_solar_activity()
        
        # Obtener análisis social MEJORADO con influencia solar real
        social_data = await hybrid_service.get_enhanced_social_analysis(solar_data)
        
        # Calcular resonancia con datos reales
        resonance = calculate_resonance(solar_data, social_data)
        current_data = {
            'solar': solar_data,
            'social': social_data,
            'resonance': resonance
        }
        
        # Analizar condiciones para alertas
        new_alerts = await alert_system.analyze_conditions(solar_data, social_data, resonance)
        
        # Guardar histórico
        historical_data.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'solar': solar_data,
            'social': social_data,
            'resonance': resonance,
            'alerts_triggered': len(new_alerts)
        })
        
        # Mantener últimos 200 puntos
        if len(historical_data) > 200:
            historical_data.pop(0)
            
    except Exception as e:
        print(f"❌ Error actualizando datos del sistema: {e}")
        # Fallback robusto
        solar_data = await nasa_service.get_current_solar_activity()
        social_data = await hybrid_service.get_enhanced_social_analysis(solar_data)
        
        resonance = calculate_resonance(solar_data, social_data)
        historical_data.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'solar': solar_data,
            'social': social_data,
            'resonance': resonance,
            'alerts_triggered': 0
        })
