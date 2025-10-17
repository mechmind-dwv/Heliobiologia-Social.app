#!/bin/bash
# scripts/run_tests.sh

echo "🧪 EJECUTANDO SUITE DE TESTS HELIOBIO-SOCIAL"
echo "============================================"

# Instalar dependencias de testing si es necesario
pip install pytest pytest-cov pytest-asyncio requests-mock

echo "1. 🔍 Ejecutando tests unitarios..."
pytest tests/unit/ -v --cov=app --cov-report=term-missing

echo "2. 🔗 Ejecutando tests de integración..."
pytest tests/integration/ -v -m integration

echo "3. 🚀 Ejecutando tests funcionales..."
pytest tests/functional/ -v -m functional

echo "4. 📊 Generando reporte de cobertura..."
pytest --cov=app --cov-report=html:coverage_report

echo "5. ✅ Verificando calidad de código..."
python -m flake8 app/ --count --max-complexity=10 --statistics

echo "🎉 TESTS COMPLETADOS!"
echo "📊 Reporte de cobertura: file://$(pwd)/coverage_report/index.html"
