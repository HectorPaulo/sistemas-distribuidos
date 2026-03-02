# 🎬 Sistema de Cine con CORBA

## Inicio Rápido

```bash
./compilar_idl.sh       # 1. Compilar IDL
python3 test_corba.py   # 2. Verificar
python3 servidor.py     # 3. Iniciar servidor
```

En otra terminal:
```bash
python3 cliente_admin.py    # Cliente administrador
# o
python3 cliente_usuario.py  # Cliente usuario
```

## Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `servidor.py` | Servidor CORBA |
| `cliente_admin.py` | Cliente administrador |
| `cliente_usuario.py` | Cliente usuario |
| `cine.idl` | Definición de interfaces |

## Documentación

📖 **[README.md](README.md)** - Documentación completa  
📘 **[GUIA_USO.md](GUIA_USO.md)** - Guía de uso con ejemplos  
📊 **[RESUMEN.md](RESUMEN.md)** - Resumen ejecutivo  
📋 **[INSTRUCCIONES.md](INSTRUCCIONES.md)** - Cómo ejecutar y entregar  

## Scripts Útiles

```bash
./compilar_idl.sh              # Compilar IDL
./iniciar.sh                   # Menú de inicio
./demo.sh                      # Demo automática
python3 test_corba.py          # Pruebas
python3 crear_datos_ejemplo.py # Crear datos de prueba
```

## Requisitos Cumplidos ✅

- ✅ Creación de películas, salas y funciones
- ✅ Generación de boletos (lado administrador)
- ✅ Funciones solo en horario del cine (08:00-23:00)
- ✅ No crear funciones en fechas pasadas
- ✅ Solo funciones en semana actual
- ✅ Mapa de asientos con filas y columnas
- ✅ Selección individual y múltiple
- ✅ Diseño limpio sin degradados

## Tecnologías

- Python 3 + omniORB
- CORBA (arquitectura distribuida)
- IDL (definición de interfaces)
- JSON (persistencia)

---

**Proyecto**: Primer Parcial - Sistemas Distribuidos  
**Fecha**: 2026-03-02  
**Estado**: ✅ Completo y funcional

