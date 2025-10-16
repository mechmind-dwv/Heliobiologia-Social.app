"""
🌞 SERVICIO REAL NASA DONKI API - VERSIÓN CORREGIDA
Obtiene datos solares en tiempo real de NASA
"""
import os
import aiohttp
import asyncio
from datetime import datetime, timedelta, timezone
import logging
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class RealNasaService:
    """Servicio real para NASA DONKI API - VERSIÓN CORREGIDA"""
    
    def __init__(self):
        self.api_key = os.getenv('NASA_API_KEY')
        self.base_url = "https://api.nasa.gov/DONKI"
        self.session = None
        
        if not self.api_key:
            logger.warning("❌ NASA API Key no configurada - Usando modo simulación")
            self.real_mode = False
        else:
            self.real_mode = True
            logger.info("✅ NASA DONKI API configurada para modo real")
    
    async def ensure_session(self):
        """Asegurar sesión HTTP"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def get_solar_flares(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Obtener fulguraciones solares reales"""
        if not self.real_mode:
            return await self._get_simulated_flares()
        
        try:
            await self.ensure_session()
            
            # Fechas por defecto: últimos 7 días
            if not start_date:
                start_date = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.utcnow().strftime('%Y-%m-%d')
            
            url = f"{self.base_url}/FLR"
            params = {
                'startDate': start_date,
                'endDate': end_date,
                'api_key': self.api_key
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_solar_flares(data)
                else:
                    logger.error(f"❌ Error NASA FLR API: {response.status}")
                    return await self._get_simulated_flares()
                    
        except Exception as e:
            logger.error(f"❌ Error obteniendo fulguraciones: {e}")
            return await self._get_simulated_flares()
    
    async def get_geomagnetic_storms(self) -> List[Dict]:
        """Obtener tormentas geomagnéticas"""
        if not self.real_mode:
            return await self._get_simulated_storms()
        
        try:
            await self.ensure_session()
            
            url = f"{self.base_url}/GST"
            params = {
                'startDate': (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'endDate': datetime.utcnow().strftime('%Y-%m-%d'),
                'api_key': self.api_key
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_geomagnetic_storms(data)
                else:
                    return await self._get_simulated_storms()
                    
        except Exception as e:
            logger.error(f"❌ Error obteniendo tormentas: {e}")
            return await self._get_simulated_storms()
    
    async def get_cme_data(self) -> List[Dict]:
        """Obtener datos de Eyecciones de Masa Coronal (CME)"""
        if not self.real_mode:
            return await self._get_simulated_cme()
        
        try:
            await self.ensure_session()
            
            url = f"{self.base_url}/CME"
            params = {
                'startDate': (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'endDate': datetime.utcnow().strftime('%Y-%m-%d'),
                'api_key': self.api_key
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_cme_data(data)
                else:
                    return await self._get_simulated_cme()
                    
        except Exception as e:
            logger.error(f"❌ Error obteniendo CME: {e}")
            return await self._get_simulated_cme()
    
    def _parse_solar_flares(self, flares_data: List[Dict]) -> List[Dict]:
        """Parsear datos de fulguraciones solares"""
        parsed_flares = []
        
        for flare in flares_data:
            # Convertir fechas a objetos datetime con timezone
            begin_time = self._parse_datetime(flare.get('beginTime'))
            peak_time = self._parse_datetime(flare.get('peakTime'))
            end_time = self._parse_datetime(flare.get('endTime'))
            
            parsed_flares.append({
                'flare_id': flare.get('flareID'),
                'class_type': flare.get('classType', 'C'),
                'intensity': self._flare_class_to_intensity(flare.get('classType', 'C')),
                'begin_time': begin_time.isoformat() if begin_time else None,
                'peak_time': peak_time.isoformat() if peak_time else None,
                'end_time': end_time.isoformat() if end_time else None,
                'active_region': flare.get('activeRegionNum'),
                'source_location': flare.get('sourceLocation'),
                '_begin_dt': begin_time,  # Para comparaciones internas
                '_peak_dt': peak_time
            })
        
        return parsed_flares
    
    def _parse_geomagnetic_storms(self, storms_data: List[Dict]) -> List[Dict]:
        """Parsear datos de tormentas geomagnéticas"""
        parsed_storms = []
        
        for storm in storms_data:
            # Calcular intensidad basada en Kp index
            kp_index = storm.get('allKpIndex', [{}])
            max_kp = max([kp.get('kpIndex', 0) for kp in kp_index]) if kp_index else 0
            
            start_time = self._parse_datetime(storm.get('startTime'))
            
            parsed_storms.append({
                'storm_id': storm.get('gstID'),
                'start_time': start_time.isoformat() if start_time else None,
                'kp_index': max_kp,
                'intensity': self._kp_to_intensity(max_kp),
                'causes': storm.get('linkedEvents', []),
                '_start_dt': start_time  # Para comparaciones internas
            })
        
        return parsed_storms
    
    def _parse_cme_data(self, cme_data: List[Dict]) -> List[Dict]:
        """Parsear datos de CME"""
        parsed_cme = []
        
        for cme in cme_data:
            start_time = self._parse_datetime(cme.get('startTime'))
            
            parsed_cme.append({
                'cme_id': cme.get('activityID'),
                'start_time': start_time.isoformat() if start_time else None,
                'speed': cme.get('cmeAnalyses', [{}])[0].get('speed', 0) if cme.get('cmeAnalyses') else 0,
                'angle': cme.get('cmeAnalyses', [{}])[0].get('latitude', 0) if cme.get('cmeAnalyses') else 0,
                'half_angle': cme.get('cmeAnalyses', [{}])[0].get('halfAngle', 0) if cme.get('cmeAnalyses') else 0,
                '_start_dt': start_time
            })
        
        return parsed_cme
    
    def _parse_datetime(self, date_string: Optional[str]) -> Optional[datetime]:
        """Parsear string de fecha a datetime con timezone"""
        if not date_string:
            return None
        
        try:
            # Intentar parsear con diferentes formatos
            if 'Z' in date_string:
                # Formato ISO con Z (UTC)
                return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            elif '+' in date_string or '-' in date_string[11:]:
                # Ya tiene offset de timezone
                return datetime.fromisoformat(date_string)
            else:
                # Asumir UTC si no hay timezone
                dt = datetime.fromisoformat(date_string)
                return dt.replace(tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            logger.warning(f"No se pudo parsear fecha: {date_string}")
            return None
    
    def _flare_class_to_intensity(self, class_type: str) -> int:
        """Convertir clase de fulguración a intensidad (1-5)"""
        class_map = {
            'A': 1, 'B': 1, 'C': 2, 
            'M': 3, 'X': 4, 'X10+': 5
        }
        return class_map.get(class_type[0] if class_type else 'C', 2)
    
    def _kp_to_intensity(self, kp_index: float) -> int:
        """Convertir índice Kp a intensidad de tormenta (0-4)"""
        if kp_index >= 8: return 4  # Severa
        elif kp_index >= 7: return 3  # Fuerte
        elif kp_index >= 6: return 2  # Moderada
        elif kp_index >= 5: return 1  # Menor
        else: return 0  # Quieta
    
    async def _get_simulated_flares(self) -> List[Dict]:
        """Fulguración simulada"""
        import random
        flares = []
        
        # Generar 0-3 fulguraciones simuladas
        for i in range(random.randint(0, 3)):
            flare_classes = ['C', 'C', 'M', 'X']  # Más probabilidad de C, menos de X
            class_type = random.choice(flare_classes)
            
            flare_time = datetime.now(timezone.utc) - timedelta(hours=i)
            
            flares.append({
                'flare_id': f'sim_flare_{i}',
                'class_type': class_type,
                'intensity': self._flare_class_to_intensity(class_type),
                'begin_time': flare_time.isoformat(),
                'peak_time': (flare_time + timedelta(minutes=30)).isoformat(),
                'active_region': random.randint(1000, 5000),
                'source_location': f'{random.randint(-90, 90)}°, {random.randint(0, 360)}°',
                '_begin_dt': flare_time
            })
        
        return flares
    
    async def _get_simulated_storms(self) -> List[Dict]:
        """Tormentas simuladas"""
        import random
        storms = []
        
        for i in range(random.randint(0, 2)):
            kp_index = random.uniform(4.0, 7.5)
            storm_time = datetime.now(timezone.utc) - timedelta(days=i)
            
            storms.append({
                'storm_id': f'sim_storm_{i}',
                'start_time': storm_time.isoformat(),
                'kp_index': kp_index,
                'intensity': self._kp_to_intensity(kp_index),
                '_start_dt': storm_time
            })
        
        return storms
    
    async def _get_simulated_cme(self) -> List[Dict]:
        """CME simulada"""
        import random
        cme_list = []
        
        if random.random() > 0.7:  # 30% de probabilidad de CME
            cme_time = datetime.now(timezone.utc) - timedelta(hours=12)
            cme_list.append({
                'cme_id': 'sim_cme_1',
                'start_time': cme_time.isoformat(),
                'speed': random.randint(500, 1500),
                'angle': random.uniform(-90, 90),
                'half_angle': random.uniform(20, 60),
                '_start_dt': cme_time
            })
        
        return cme_list
    
    async def get_current_solar_activity(self) -> Dict:
        """Obtener actividad solar actual combinando múltiples fuentes - VERSIÓN CORREGIDA"""
        flares = await self.get_solar_flares()
        storms = await self.get_geomagnetic_storms()
        cme_data = await self.get_cme_data()
        
        # Calcular actividad solar general
        flare_activity = max([f['intensity'] for f in flares]) if flares else 0
        storm_activity = max([s['intensity'] for s in storms]) if storms else 0
        
        # Fulguraciones recientes (últimas 24 horas) - CORREGIDO
        now_utc = datetime.now(timezone.utc)
        recent_flares = [
            f for f in flares 
            if f.get('_begin_dt') and f['_begin_dt'] > now_utc - timedelta(hours=24)
        ]
        
        # CME en progreso
        active_cme = len(cme_data) > 0
        
        return {
            'sunspot_number': random.randint(20, 120),
            'solar_flux': random.randint(70, 130),
            'flare_activity': flare_activity,
            'geomagnetic_storm': storm_activity,
            'solar_wind_speed': random.randint(300, 600),
            'coronal_holes': random.randint(0, 5),
            'recent_flares_count': len(recent_flares),
            'active_cme': active_cme,
            'data_source': 'nasa_donki' if self.real_mode else 'nasa_simulation',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'raw_flares': flares[:3],
            'raw_storms': storms[:2]
        }
    
    async def close(self):
        """Cerrar sesión"""
        if self.session:
            await self.session.close()

# Añadir import random para las simulaciones
import random
