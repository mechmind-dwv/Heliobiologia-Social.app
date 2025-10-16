#!/bin/bash
echo "🌌 CREANDO BACKUP CÓSMICO..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="heliobio_backup_$TIMESTAMP"

mkdir -p $BACKUP_DIR

# Copiar archivos esenciales
cp -r app $BACKUP_DIR/
cp -r scripts $BACKUP_DIR/ 
cp -r data $BACKUP_DIR/
cp requirements.txt $BACKUP_DIR/
cp README.md $BACKUP_DIR/
cp MANIFESTO.md $BACKUP_DIR/
cp .env $BACKUP_DIR/ 2>/dev/null || echo "⚠️  .env no encontrado - configurar manualmente"

# Crear archivo comprimido
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR

echo "✅ Backup creado: $BACKUP_DIR.tar.gz"
echo "📦 Contenido:"
ls -la $BACKUP_DIR/
