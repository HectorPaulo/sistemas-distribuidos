#!/bin/bash
# Script para demostración rápida del sistema

echo "============================================================"
echo "DEMOSTRACION DEL SISTEMA DE CINE"
echo "============================================================"
echo ""
echo "Este script iniciará el servidor y creará datos de ejemplo"
echo ""

# Verificar compilación IDL
if [ ! -f "cine_idl.py" ]; then
    echo "Compilando IDL..."
    ./compilar_idl.sh
fi

# Iniciar servidor en segundo plano
echo "Iniciando servidor..."
python3 servidor.py &
SERVIDOR_PID=$!

echo "Esperando que el servidor inicie..."
sleep 3

# Crear datos de ejemplo
echo ""
echo "Creando datos de ejemplo..."
echo "s" | python3 crear_datos_ejemplo.py

echo ""
echo "============================================================"
echo "✓ SISTEMA LISTO"
echo "============================================================"
echo ""
echo "El servidor está corriendo (PID: $SERVIDOR_PID)"
echo ""
echo "Para usar el sistema, abra nuevas terminales y ejecute:"
echo ""
echo "  Cliente Administrador:"
echo "    python3 cliente_admin.py"
echo ""
echo "  Cliente Usuario:"
echo "    python3 cliente_usuario.py"
echo ""
echo "Para detener el servidor:"
echo "    kill $SERVIDOR_PID"
echo ""
echo "============================================================"

# Mantener el script corriendo
wait $SERVIDOR_PID

