#!/bin/bash

echo "🧪 EJECUTANDO SUITE DE TESTS HELIOBIO-SOCIAL (CORREGIDA)"
echo "========================================================"

# Configurar para evitar conflictos con ROS
export PYTEST_ADDOPTS="-p no:launch_testing"

echo "1. 🔍 Ejecutando tests unitarios..."
python -m pytest tests/unit/ -v --tb=short -p no:launch_testing

echo "2. 🔗 Ejecutando tests de integración..."
python -m pytest tests/integration/ -v -p no:launch_testing

echo "3. 🚀 Ejecutando tests funcionales..."
python -m pytest tests/functional/ -v -p no:launch_testing

echo "4. 📊 Generando reporte de cobertura..."
python -m pytest --cov=app --cov-report=html:coverage_report -p no:launch_testing

echo "🎉 TESTS COMPLETADOS!"
echo "📊 Reporte: file://$(pwd)/coverage_report/index.html"
