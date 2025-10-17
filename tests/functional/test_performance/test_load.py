# tests/functional/test_performance/test_load.py
import pytest
import time
from fastapi.testclient import TestClient

class TestPerformance:
    
    def test_response_time_health(self, client):
        """Test tiempo de respuesta del endpoint de salud"""
        start_time = time.time()
        response = client.get("/api/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Menos de 1 segundo
    
    def test_concurrent_requests(self, client):
        """Test de requests concurrentes"""
        import threading
        
        results = []
        
        def make_request():
            response = client.get("/api/health")
            results.append(response.status_code)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert all(result == 200 for result in results)
        assert len(results) == 10
    
    def test_memory_usage(self, client):
        """Test básico de uso de memoria"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Hacer varias requests
        for _ in range(100):
            client.get("/api/health")
        
        final_memory = process.memory_info().rss / 1024 / 1024
        
        # No debería haber fugas de memoria significativas
        memory_increase = final_memory - initial_memory
        assert memory_increase < 50  # Menos de 50MB de aumento
