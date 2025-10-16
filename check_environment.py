"""
🔍 VERIFICADOR DE ENTORNO HELIOBIO-SOCIAL
"""
import sys

def check_package(package_name):
    try:
        __import__(package_name)
        return True, f"✅ {package_name}"
    except ImportError:
        return False, f"❌ {package_name}"

# Paquetes críticos
critical_packages = [
    "aiohttp", "fastapi", "uvicorn", "pandas", "numpy",
    "textblob", "nltk", "plotly", "sklearn", "scipy"
]

print("🔍 VERIFICANDO ENTORNO HELIOBIO-SOCIAL...")
print("=" * 50)

all_ok = True
for package in critical_packages:
    ok, message = check_package(package)
    print(message)
    if not ok:
        all_ok = False

print("=" * 50)
if all_ok:
    print("🎉 ENTORNO LISTO PARA HELIOBIO-SOCIAL v1.3.0")
    print("🚀 Ejecuta: ./scripts/start_development.sh")
else:
    print("❌ Faltan dependencias críticas")
    print("💡 Ejecuta: ./scripts/fix_environment.sh")
