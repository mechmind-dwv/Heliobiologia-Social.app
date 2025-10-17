#!/bin/bash
echo "🔍 VERIFICANDO RECUPERACIÓN..."
echo "==============================="

critical_files=(
    "app/main.py"
    "requirements.txt" 
    "scripts/run_tests_fixed.sh"
    "tests/conftest.py"
    ".github/workflows/tests.yml"
    "pytest.ini"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - FALTANTE"
    fi
done

echo "📊 ESTRUCTURA DE DIRECTORIOS:"
[ -d "app" ] && echo "✅ app/" || echo "❌ app/"
[ -d "tests" ] && echo "✅ tests/" || echo "❌ tests/" 
[ -d "scripts" ] && echo "✅ scripts/" || echo "❌ scripts/"

echo "🎉 VERIFICACIÓN COMPLETADA"
