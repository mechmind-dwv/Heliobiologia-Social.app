"""
🌐 SERVICIO REAL FACEBOOK GRAPH API - VERSIÓN CORREGIDA
Conecta con la API real de Facebook usando tokens válidos
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

class RealFacebookService:
    """Servicio real para Facebook Graph API - VERSIÓN CORREGIDA"""
    
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID', '').strip('"')  # Limpiar comillas
        
        self.base_url = "https://graph.facebook.com/v19.0"
        self.session = None
        
        # Verificar configuración
        if not all([self.app_id, self.app_secret, self.access_token]):
            logger.warning("❌ Credenciales de Facebook incompletas - Usando modo simulación")
            self.real_mode = False
        else:
            self.real_mode = True
            logger.info(f"✅ Facebook Graph API configurada - Page ID: {self.page_id}")
    
    async def ensure_session(self):
        """Asegurar sesión HTTP"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def validate_token(self):
        """Validar token de acceso"""
        if not self.real_mode:
            return False
            
        try:
            await self.ensure_session()
            url = f"{self.base_url}/debug_token"
            params = {
                'input_token': self.access_token,
                'access_token': f"{self.app_id}|{self.app_secret}"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    is_valid = data.get('data', {}).get('is_valid', False)
                    if is_valid:
                        logger.info("✅ Token de Facebook válido")
                    else:
                        logger.error("❌ Token de Facebook inválido")
                    return is_valid
                else:
                    logger.error(f"❌ Error validando token: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error en validación de token: {e}")
            return False
    
    async def get_page_insights(self) -> Dict:
        """Obtener métricas de la página - VERSIÓN CORREGIDA"""
        if not self.real_mode or not await self.validate_token():
            return await self._get_simulated_insights()
        
        try:
            await self.ensure_session()
            
            # Primero obtener información básica de la página
            page_url = f"{self.base_url}/{self.page_id}"
            page_params = {
                'fields': 'id,name,fan_count,engagement,posts.limit(5){likes,comments,shares,created_time}',
                'access_token': self.access_token
            }
            
            async with self.session.get(page_url, params=page_params) as response:
                if response.status == 200:
                    page_data = await response.json()
                    return self._parse_page_data(page_data)
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Error Facebook API: {response.status} - {error_text}")
                    return await self._get_simulated_insights()
                    
        except Exception as e:
            logger.error(f"❌ Error obteniendo insights: {e}")
            return await self._get_simulated_insights()
    
    async def get_page_posts(self, limit: int = 10) -> List[Dict]:
        """Obtener posts recientes de la página - VERSIÓN CORREGIDA"""
        if not self.real_mode or not await self.validate_token():
            return await self._get_simulated_posts(limit)
        
        try:
            await self.ensure_session()
            
            posts_url = f"{self.base_url}/{self.page_id}/posts"
            posts_params = {
                'fields': 'id,message,created_time,likes.limit(1).summary(true),comments.limit(1).summary(true),shares',
                'limit': limit,
                'access_token': self.access_token
            }
            
            async with self.session.get(posts_url, params=posts_params) as response:
                if response.status == 200:
                    posts_data = await response.json()
                    return self._parse_posts_data(posts_data.get('data', []))
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Error obteniendo posts: {response.status} - {error_text}")
                    return await self._get_simulated_posts(limit)
                    
        except Exception as e:
            logger.error(f"❌ Error obteniendo posts: {e}")
            return await self._get_simulated_posts(limit)
    
    def _parse_page_data(self, page_data: Dict) -> Dict:
        """Parsear datos de la página"""
        fan_count = page_data.get('fan_count', 0)
        posts = page_data.get('posts', {}).get('data', [])
        
        # Calcular engagement reciente
        recent_engagement = 0
        emotion_analysis = []
        
        for post in posts[:5]:  # Últimos 5 posts
            likes = post.get('likes', {}).get('summary', {}).get('total_count', 0)
            comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
            shares = post.get('shares', {}).get('count', 0)
            recent_engagement += likes + comments + shares
            
            # Análisis básico de emociones basado en engagement
            if likes > 100:
                emotion_analysis.append('positive')
            elif comments > 50:
                emotion_analysis.append('discussion')
            else:
                emotion_analysis.append('neutral')
        
        # Determinar emoción dominante
        dominant_emotion = max(set(emotion_analysis), key=emotion_analysis.count) if emotion_analysis else 'neutral'
        
        return {
            'page_name': page_data.get('name', 'Unknown Page'),
            'fan_count': fan_count,
            'recent_engagement': recent_engagement,
            'engagement_intensity': min(100, recent_engagement / max(1, fan_count) * 1000),
            'dominant_emotion': dominant_emotion,
            'post_count_recent': len(posts),
            'data_source': 'facebook_graph_api',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def _parse_posts_data(self, posts_data: List[Dict]) -> List[Dict]:
        """Parsear datos de posts"""
        parsed_posts = []
        
        for post in posts_data:
            created_time = self._parse_facebook_date(post.get('created_time'))
            likes = post.get('likes', {}).get('summary', {}).get('total_count', 0)
            comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
            shares = post.get('shares', {}).get('count', 0)
            
            parsed_posts.append({
                'id': post.get('id'),
                'message': post.get('message', '')[:100] + '...' if post.get('message') else 'No text',
                'created_time': created_time.isoformat() if created_time else None,
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'total_engagement': likes + comments + shares,
                'sentiment': self._estimate_sentiment(likes, comments, shares)
            })
        
        return parsed_posts
    
    def _parse_facebook_date(self, date_string: Optional[str]) -> Optional[datetime]:
        """Parsear fecha de Facebook a datetime con timezone"""
        if not date_string:
            return None
        
        try:
            # Formato de Facebook: 2024-01-15T10:30:00+0000
            if '+' in date_string:
                dt_str = date_string.replace('+0000', '+00:00')
                return datetime.fromisoformat(dt_str)
            else:
                dt = datetime.fromisoformat(date_string)
                return dt.replace(tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            logger.warning(f"No se pudo parsear fecha de Facebook: {date_string}")
            return None
    
    def _estimate_sentiment(self, likes: int, comments: int, shares: int) -> str:
        """Estimar sentimiento basado en engagement"""
        total = likes + comments * 2 + shares * 3
        
        if total > 100:
            return 'highly_positive'
        elif total > 50:
            return 'positive'
        elif total > 20:
            return 'neutral'
        else:
            return 'low_engagement'
    
    async def _get_simulated_insights(self) -> Dict:
        """Insights simulados para cuando Facebook API falle"""
        import random
        
        # Datos simulados realistas
        fan_count = random.randint(1000, 50000)
        recent_engagement = random.randint(50, 5000)
        
        emotions = ['positive', 'neutral', 'discussion', 'excited']
        dominant_emotion = random.choice(emotions)
        
        return {
            'page_name': 'Página de Muestra',
            'fan_count': fan_count,
            'recent_engagement': recent_engagement,
            'engagement_intensity': min(100, recent_engagement / max(1, fan_count) * 1000),
            'dominant_emotion': dominant_emotion,
            'post_count_recent': random.randint(3, 15),
            'trending_topics': [
                {'topic': 'Actualidad', 'mentions': random.randint(10, 100)},
                {'topic': 'Tecnología', 'mentions': random.randint(5, 50)},
                {'topic': 'Ciencia', 'mentions': random.randint(3, 30)}
            ],
            'data_source': 'facebook_simulation',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def _get_simulated_posts(self, limit: int = 10) -> List[Dict]:
        """Posts simulados"""
        import random
        
        posts = []
        base_time = datetime.now(timezone.utc)
        
        for i in range(limit):
            post_time = base_time - timedelta(hours=i*2)
            likes = random.randint(10, 500)
            comments = random.randint(0, 50)
            shares = random.randint(0, 30)
            
            posts.append({
                'id': f'sim_post_{i}',
                'message': f'Publicación simulada #{i} sobre temas actuales y relevantes...',
                'created_time': post_time.isoformat(),
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'total_engagement': likes + comments + shares,
                'sentiment': self._estimate_sentiment(likes, comments, shares)
            })
        
        return posts
    
    async def get_social_analysis(self) -> Dict:
        """Análisis social completo - VERSIÓN CORREGIDA"""
        insights = await self.get_page_insights()
        posts = await self.get_page_posts(5)
        
        # Enriquecer análisis con datos de posts
        total_engagement = sum(post['total_engagement'] for post in posts)
        avg_sentiment = sum(1 for post in posts if post['sentiment'] in ['positive', 'highly_positive']) / len(posts) if posts else 0.5
        
        return {
            **insights,
            'recent_posts_analysis': {
                'total_posts_analyzed': len(posts),
                'total_engagement': total_engagement,
                'average_sentiment_score': avg_sentiment,
                'engagement_trend': 'increasing' if total_engagement > 100 else 'stable'
            },
            'collective_mood_indicator': self._calculate_mood_indicator(insights, posts),
            'social_tension_index': random.uniform(0.1, 0.8) if not self.real_mode else self._calculate_tension_index(posts)
        }
    
    def _calculate_mood_indicator(self, insights: Dict, posts: List[Dict]) -> str:
        """Calcular indicador de humor colectivo"""
        engagement = insights.get('engagement_intensity', 0)
        emotion = insights.get('dominant_emotion', 'neutral')
        
        if engagement > 70 and emotion == 'positive':
            return 'highly_positive'
        elif engagement > 50:
            return 'engaged'
        elif emotion == 'discussion':
            return 'discursive'
        else:
            return 'neutral'
    
    def _calculate_tension_index(self, posts: List[Dict]) -> float:
        """Calcular índice de tensión social (simulado para ahora)"""
        import random
        return random.uniform(0.1, 0.6)
    
    async def close(self):
        """Cerrar sesión"""
        if self.session:
            await self.session.close()

# Añadir import random para las simulaciones
import random
