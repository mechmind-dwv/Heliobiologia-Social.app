#!/bin/bash
echo "🌞 INSTALANDO HELIOBIO-SOCIAL v1.0.0"
echo "=========================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instala Python 3.8+ primero."
    exit 1
fi

# Crear entorno virtual
echo "🧠 Creando entorno virtual consciente..."
python3 -m venv cosmos_venv

# Activar entorno
echo "⚡ Activando conciencia cósmica..."
source cosmos_venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias espirituales..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar ambiente
echo "🔮 Configurando conexiones cósmicas..."
mkdir -p data logs

echo "🎉 ¡Instalación completada!"
echo ""
echo "🚀 PARA ACTIVAR EL SISTEMA:"
echo "   source cosmos_venv/bin/activate"
echo "   ./scripts/start_development.sh"
echo ""
echo "🌐 Dashboard: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
