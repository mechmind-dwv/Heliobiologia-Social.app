# Probar componentes individualmente
from core.consciousness_verifier import ConsciousnessVerifier

verifier = ConsciousnessVerifier()
results = verifier.verify_full_system()

if results["cosmic_connection"] == "active":
    print("🌌 CONEXIÓN CÓSMICA ESTABLECIDA")
