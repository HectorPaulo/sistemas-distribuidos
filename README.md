# Sistema de Cine con CORBA

Sistema completo de gestión de cine implementado con CORBA (Common Object Request Broker Architecture) en Python.

## Características

### Funcionalidades Implementadas

✅ **Gestión de Películas**
- Crear películas con título, género y duración
- Listar todas las películas disponibles

✅ **Gestión de Salas**
- Crear salas con nombre, filas y columnas
- Máximo 26 filas (A-Z) y 20 columnas
- Listar todas las salas

✅ **Gestión de Funciones**
- Crear funciones solo en la semana actual
- Validación de horario (08:00 - 23:00)
- No permite crear funciones en fechas pasadas
- Previene conflictos de horario en la misma sala

✅ **Sistema de Boletos**
- Visualización de mapa de asientos con filas y columnas
- Selección individual o múltiple de asientos
- Generación de boletos con información completa
- Validación de disponibilidad de asientos

### Validaciones

- ✅ Funciones solo en horario de actividades del cine (08:00 - 23:00)
- ✅ No permite crear funciones en fechas pasadas
- ✅ Solo permite crear funciones en la semana actual
- ✅ Mapa de asientos visual identificando filas (A-Z) y columnas (1-n)
- ✅ Selección de asientos con verificación de disponibilidad
- ✅ Diseño limpio de boletos sin efectos visuales complejos

## Requisitos

### Software Necesario

- Python 3.6 o superior
- omniORB y omniORBpy
- Sistema operativo Linux (recomendado)

### Instalación de Dependencias

#### En Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install python3-omniorb omniidl omniorb-nameserver
```

#### Con pip (alternativa):

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
PrimerParcialSistemasDistribuidos/
│
├── cine.idl                 # Definición de interfaces CORBA
├── compilar_idl.sh         # Script para compilar IDL
├── servidor.py             # Servidor CORBA
├── cliente_admin.py        # Cliente administrador
├── cliente_usuario.py      # Cliente usuario
├── requirements.txt        # Dependencias Python
└── README.md              # Este archivo
```

## Instalación y Configuración

### 1. Clonar o descargar el proyecto

```bash
cd /home/paulo/PycharmProjects/PrimerParcialSistemasDistribuidos
```

### 2. Instalar dependencias

```bash
sudo apt-get install python3-omniorb omniidl omniorb-nameserver
```

### 3. Compilar el archivo IDL

```bash
chmod +x compilar_idl.sh
./compilar_idl.sh
```

Esto generará los archivos:
- `Cine_idl.py`
- `Cine__POA.py`

## Uso del Sistema

### Opción 1: Con Servicio de Nombres (Recomendado)

#### 1. Iniciar el servicio de nombres CORBA

```bash
omniNames -start 2809
```

Si ya está corriendo, solo ejecute:
```bash
omniNames
```

#### 2. Iniciar el servidor

```bash
python3 servidor.py
```

#### 3. En otra terminal, iniciar el cliente administrador

```bash
python3 cliente_admin.py
```

#### 4. En otra terminal, iniciar el cliente usuario

```bash
python3 cliente_usuario.py
```

### Opción 2: Sin Servicio de Nombres

Si el servicio de nombres no está disponible, el servidor automáticamente guardará su IOR en `servidor.ior` y los clientes lo leerán automáticamente.

#### 1. Iniciar el servidor

```bash
python3 servidor.py
```

#### 2. Iniciar clientes (en otras terminales)

```bash
python3 cliente_admin.py
# o
python3 cliente_usuario.py
```

## Guía de Uso

### Cliente Administrador

1. **Crear Películas**
   - Seleccionar opción 1 → 1
   - Ingresar título, género y duración

2. **Crear Salas**
   - Seleccionar opción 2 → 1
   - Ingresar nombre, número de filas y columnas

3. **Crear Funciones**
   - Seleccionar opción 3 → 1
   - Elegir película y sala
   - Ingresar fecha (YYYY-MM-DD) y hora (HH:MM)
   - La fecha debe estar en la semana actual
   - La hora debe estar entre 08:00 y 23:00

4. **Generar Boletos**
   - Seleccionar opción 4
   - Elegir función
   - Ver mapa de asientos
   - Seleccionar asientos (ej: A5, B10)
   - Ingresar datos del cliente

### Cliente Usuario

1. **Ver Cartelera**
   - Muestra todas las películas disponibles

2. **Ver Funciones**
   - Lista funciones con disponibilidad de asientos
   - Puede filtrar por fecha

3. **Comprar Boletos**
   - Seleccionar función
   - Ver mapa de asientos disponibles
   - Elegir asientos
   - Confirmar compra
   - Recibir boletos

## Formato del Mapa de Asientos

```
============================================================
MAPA DE ASIENTOS
============================================================
[ ] = Disponible    [X] = Ocupado
------------------------------------------------------------
      1  2  3  4  5  6  7  8  9 10
 A   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
 B   [ ][ ][X][X][ ][ ][ ][ ][ ][ ]
 C   [ ][ ][ ][ ][X][ ][ ][ ][ ][ ]
 D   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]

------------------------------------------------------------
PANTALLA
============================================================
```

## Formato del Boleto

```
============================================================
BOLETO
============================================================
Boleto #: 1
Cliente: Juan Pérez
------------------------------------------------------------
Película: Avatar 2
Género: Ciencia Ficción
Duración: 180 minutos
------------------------------------------------------------
Sala: Sala 1
Fecha: 2026-03-02
Hora: 18:00
Asiento: B5
------------------------------------------------------------
Precio: $50.00
============================================================
Gracias por su compra!
============================================================
```

## Persistencia de Datos

El servidor guarda automáticamente todos los datos en `datos_cine.json`, incluyendo:
- Películas
- Salas
- Funciones
- Boletos
- Asientos ocupados

Los datos se cargan automáticamente al iniciar el servidor.

## Detalles Técnicos

### Arquitectura CORBA

- **IDL (Interface Definition Language)**: Define las interfaces y tipos de datos
- **Servidor**: Implementa las interfaces y gestiona la lógica de negocio
- **Clientes**: Se conectan al servidor para consumir servicios

### Validaciones Implementadas

1. **Validación de Fechas**:
   - No permite fechas pasadas
   - Solo permite fechas de la semana actual

2. **Validación de Horarios**:
   - Horario del cine: 08:00 - 23:00
   - Previene conflictos en la misma sala

3. **Validación de Asientos**:
   - Verifica disponibilidad
   - Previene doble reservación
   - Valida filas y columnas

### Manejo de Errores

- Uso de excepciones CORBA personalizadas (`ErrorValidacion`)
- Validación de entrada del usuario
- Mensajes de error descriptivos
- Transacciones seguras (rollback en caso de error)

## Problemas Comunes y Soluciones

### Error: "No module named 'omniORB'"

Solución:
```bash
sudo apt-get install python3-omniorb
```

### Error: "Cannot contact name service"

Solución:
```bash
# Reiniciar el servicio de nombres
killall omniNames
omniNames -start 2809
```

El sistema automáticamente usará archivos IOR si el servicio de nombres no está disponible.

### Error al compilar IDL

Solución:
```bash
sudo apt-get install omniidl
```

## Notas Adicionales

- El sistema mantiene el estado entre reinicios mediante `datos_cine.json`
- Los precios de boletos están configurados en $50.00 por defecto
- El horario del cine es de 08:00 a 23:00
- Máximo 26 filas (A-Z) y 20 columnas por sala

## Autor

Sistema desarrollado para el Primer Parcial de Sistemas Distribuidos

## Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

