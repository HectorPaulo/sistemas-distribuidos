#!/bin/bash
# Script de inicio rápido del sistema

echo "============================================================"
echo "SISTEMA DE CINE - INICIO RAPIDO"
echo "============================================================"
echo ""

# Verificar si está instalado omniORB
if ! command -v omniidl &> /dev/null; then
    echo "⚠ omniidl no está instalado"
    echo "Instalando dependencias..."
    sudo apt-get update
    sudo apt-get install -y python3-omniorb omniidl omniorb-nameserver
fi

# Compilar IDL si no existe
if [ ! -f "Cine_idl.py" ]; then
    echo "Compilando archivo IDL..."
    omniidl -bpython cine.idl

    if [ $? -eq 0 ]; then
        echo "✓ IDL compilado exitosamente"
    else
        echo "✗ Error al compilar IDL"
        exit 1
    fi
else
    echo "✓ IDL ya compilado"
fi

echo ""
echo "============================================================"
echo "OPCIONES DE INICIO"
echo "============================================================"
echo "1. Iniciar servidor"
echo "2. Iniciar cliente administrador"
echo "3. Iniciar cliente usuario"
echo "4. Iniciar todo (servidor + servicio de nombres)"
echo "0. Salir"
echo "============================================================"

read -p "Seleccione una opción: " opcion

case $opcion in
    1)
        echo "Iniciando servidor..."
        python3 servidor.py
        ;;
    2)
        echo "Iniciando cliente administrador..."
        python3 cliente_admin.py
        ;;
    3)
        echo "Iniciando cliente usuario..."
        python3 cliente_usuario.py
        ;;
    4)
        echo "Iniciando servicio de nombres..."
        # Verificar si omniNames está corriendo
        if pgrep omniNames > /dev/null; then
            echo "✓ Servicio de nombres ya está corriendo"
        else
            omniNames -start 2809 &
            sleep 2
            echo "✓ Servicio de nombres iniciado"
        fi

        echo "Iniciando servidor..."
        python3 servidor.py
        ;;
    0)
        echo "Saliendo..."
        exit 0
        ;;
    *)
        echo "Opción inválida"
        exit 1
        ;;
esac

