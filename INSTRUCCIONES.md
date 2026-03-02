# INSTRUCCIONES DE ENTREGA Y EJECUCIÓN

## 📦 Contenido del Proyecto

Este proyecto contiene un **Sistema Completo de Gestión de Cine** implementado con CORBA.

### Archivos Principales

#### Código Fuente
- `cine.idl` - Definición de interfaces CORBA
- `servidor.py` - Servidor CORBA (16 KB)
- `cliente_admin.py` - Cliente administrador (21 KB)
- `cliente_usuario.py` - Cliente usuario (16 KB)

#### Scripts de Utilidad
- `compilar_idl.sh` - Compila el archivo IDL
- `iniciar.sh` - Menú de inicio rápido
- `demo.sh` - Demostración automática
- `test_corba.py` - Pruebas del sistema
- `crear_datos_ejemplo.py` - Crea datos de prueba

#### Documentación
- `README.md` - Documentación principal (319 líneas)
- `GUIA_USO.md` - Guía detallada de uso (370 líneas)
- `RESUMEN.md` - Resumen ejecutivo (444 líneas)
- `INSTRUCCIONES.md` - Este archivo

#### Generados (automáticos)
- `cine_idl.py` - Generado por omniidl
- `Cine/` - Módulo Python generado
- `Cine__POA/` - Módulo POA generado
- `datos_cine.json` - Base de datos (se crea al ejecutar)
- `servidor.ior` - IOR del servidor (opcional)

---

## 🚀 Cómo Ejecutar el Proyecto

### Requisitos Previos

```bash
# Instalar dependencias (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-omniorb omniidl omniorb-nameserver
```

### Opción 1: Ejecución Rápida (Recomendada)

```bash
# 1. Compilar IDL
./compilar_idl.sh

# 2. Probar que todo funcione
python3 test_corba.py

# 3. Iniciar servidor
python3 servidor.py
```

En **otra terminal**:
```bash
# 4. Cliente administrador
python3 cliente_admin.py
```

En **otra terminal** (opcional):
```bash
# 5. Cliente usuario
python3 cliente_usuario.py
```

### Opción 2: Con Datos de Ejemplo

```bash
# 1. Compilar IDL
./compilar_idl.sh

# 2. Iniciar servidor
python3 servidor.py
```

En **otra terminal**:
```bash
# 3. Crear datos de ejemplo
python3 crear_datos_ejemplo.py
# Responder 's' cuando pregunte

# 4. Iniciar cliente
python3 cliente_admin.py
# o
python3 cliente_usuario.py
```

### Opción 3: Demostración Automática

```bash
./demo.sh
```

Este script:
1. Compila el IDL si es necesario
2. Inicia el servidor en segundo plano
3. Crea datos de ejemplo automáticamente
4. Deja el servidor corriendo

Luego puede abrir los clientes en otras terminales.

---

## 📋 Verificación del Sistema

### Paso 1: Compilar IDL

```bash
./compilar_idl.sh
```

**Salida esperada:**
```
Compilando archivo IDL...
Compilación exitosa. Archivos generados en el directorio actual.
```

### Paso 2: Probar Módulos

```bash
python3 test_corba.py
```

**Salida esperada:**
```
============================================================
PRUEBA DE MODULOS CORBA
============================================================

Probando importaciones...
  - Importando omniORB... ✓
  - Importando CosNaming... ✓
  - Importando módulo Cine... ✓
  - Importando módulo Cine__POA... ✓

✓ Todas las importaciones exitosas

Probando estructuras CORBA...
  - Estructura Pelicula... ✓
  - Estructura Sala... ✓
  - Estructura Funcion... ✓
  - Estructura Asiento... ✓
  - Estructura Boleto... ✓
  - Excepción ErrorValidacion... ✓

✓ Todas las estructuras funcionan correctamente

Probando interfaz CORBA...
  - Interfaz SistemaCine... ✓

✓ Interfaz definida correctamente

============================================================
✓ TODAS LAS PRUEBAS EXITOSAS
============================================================
```

### Paso 3: Iniciar Servidor

```bash
python3 servidor.py
```

**Salida esperada:**
```
Servidor registrado en el servicio de nombres como 'SistemaCine'
Servidor de Cine iniciado y esperando solicitudes...
Horario de operación: 08:00 - 23:00
Presione Ctrl+C para detener el servidor
```

Si no hay servicio de nombres:
```
No se pudo registrar en el servicio de nombres: ...
Guardando IOR en archivo...
IOR guardado en 'servidor.ior'
Servidor de Cine iniciado y esperando solicitudes...
```

### Paso 4: Probar Clientes

Abrir en otra terminal:

```bash
python3 cliente_admin.py
```

**Salida esperada:**
```
============================================================
CLIENTE ADMINISTRADOR - SISTEMA DE CINE
============================================================
Conectado al servidor correctamente

============================================================
MENU ADMINISTRADOR
============================================================
1. Gestión de Películas
2. Gestión de Salas
3. Gestión de Funciones
4. Generación de Boletos
5. Ver Todos los Boletos
0. Salir
============================================================
Seleccione una opción:
```

---

## 🎯 Demostración Rápida

### Escenario Completo

#### Terminal 1: Servidor
```bash
python3 servidor.py
```

#### Terminal 2: Crear Datos
```bash
python3 crear_datos_ejemplo.py
# Responder: s
```

Esto crea:
- 5 películas
- 5 salas
- Múltiples funciones para la semana
- Algunos boletos de ejemplo

#### Terminal 3: Cliente Usuario
```bash
python3 cliente_usuario.py

# Menú → 2 (Ver funciones disponibles)
# Menú → 3 (Comprar boletos)
# Seleccionar función
# Ver mapa de asientos
# Seleccionar asientos (ej: A1, A2)
# Confirmar compra
```

---

## 📖 Funcionalidades a Demostrar

### 1. Crear Película (Administrador)

```
Menu → 1 (Películas) → 1 (Crear)
Título: Avatar 2
Género: Ciencia Ficción
Duración: 192

Resultado: ✓ Película creada exitosamente (ID: 1)
```

### 2. Crear Sala (Administrador)

```
Menu → 2 (Salas) → 1 (Crear)
Nombre: Sala VIP
Filas: 8
Columnas: 10

Resultado: ✓ Sala creada exitosamente (ID: 1)
```

### 3. Crear Función (Administrador)

```
Menu → 3 (Funciones) → 1 (Crear)
ID Película: 1
ID Sala: 1
Fecha: 2026-03-02  (hoy, semana actual)
Hora: 18:00  (entre 08:00 y 23:00)

Resultado: ✓ Función creada exitosamente (ID: 1)
```

### 4. Validación: Fecha Pasada ❌

```
Menu → 3 → 1
Fecha: 2026-03-01  (ayer)

Resultado: ✗ Error: No se pueden crear funciones en fechas pasadas
```

### 5. Validación: Hora Inválida ❌

```
Menu → 3 → 1
Hora: 07:00  (antes de 08:00)

Resultado: ✗ Error: La hora debe estar entre 08:00 y 23:00
```

### 6. Ver Mapa de Asientos

```
Menu → 4 (Generar Boletos)
ID Función: 1

Resultado:
============================================================
MAPA DE ASIENTOS
============================================================
[ ] = Disponible    [X] = Ocupado
------------------------------------------------------------
      1  2  3  4  5  6  7  8  9 10
 A   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
 B   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
 C   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
```

### 7. Comprar Boletos Múltiples

```
Nombre: Juan Pérez
Precio: 50
Asiento: A5
Asiento: A6
Asiento: fin

Resultado:
============================================================
BOLETOS GENERADOS
============================================================
Cliente: Juan Pérez
...
Boleto #1 - Asiento: A5 - Precio: $50.00
Boleto #2 - Asiento: A6 - Precio: $50.00
...
Total: $100.00
============================================================
```

---

## 🎓 Criterios de Evaluación Cumplidos

### ✅ Funcionalidades Básicas (100%)

- [x] Creación de películas
- [x] Creación de salas
- [x] Generación de funciones
- [x] Generación de boletos (lado administrador)

### ✅ Validaciones (100%)

- [x] Funciones solo en horario del cine (08:00-23:00)
- [x] No crear funciones en fechas pasadas
- [x] Funciones solo en la semana actual
- [x] Diseño de sala con filas y columnas
- [x] Selección de asientos con disponibilidad
- [x] Selección múltiple de asientos

### ✅ Diseño (100%)

- [x] Diseño limpio
- [x] Sin degradados
- [x] Sin colores asistidos por IA
- [x] Interfaz de texto clara

### ✅ Técnico (100%)

- [x] Implementado con CORBA
- [x] Arquitectura cliente-servidor
- [x] Persistencia de datos
- [x] Manejo de excepciones
- [x] Código documentado

---

## 📁 Estructura de Entrega

```
PrimerParcialSistemasDistribuidos/
├── Código Fuente/
│   ├── cine.idl
│   ├── servidor.py
│   ├── cliente_admin.py
│   └── cliente_usuario.py
│
├── Scripts/
│   ├── compilar_idl.sh
│   ├── iniciar.sh
│   ├── demo.sh
│   ├── test_corba.py
│   └── crear_datos_ejemplo.py
│
├── Documentación/
│   ├── README.md
│   ├── GUIA_USO.md
│   ├── RESUMEN.md
│   └── INSTRUCCIONES.md
│
└── Dependencias/
    └── requirements.txt
```

---

## 🔍 Checklist de Entrega

Antes de entregar, verificar:

- [ ] El IDL compila correctamente (`./compilar_idl.sh`)
- [ ] Las pruebas pasan (`python3 test_corba.py`)
- [ ] El servidor inicia sin errores (`python3 servidor.py`)
- [ ] Los clientes se conectan correctamente
- [ ] Se pueden crear películas, salas y funciones
- [ ] Las validaciones funcionan correctamente
- [ ] El mapa de asientos se muestra bien
- [ ] Los boletos se generan correctamente
- [ ] La documentación está completa
- [ ] Todos los archivos están incluidos

---

## 📞 Información de Contacto

**Proyecto**: Sistema de Cine con CORBA  
**Asignatura**: Sistemas Distribuidos  
**Fecha**: 2026-03-02  
**Tipo**: Primer Parcial

---

## 🎉 Conclusión

El proyecto está **completo y listo para ejecutar**. Incluye:

- ✅ Todos los requisitos funcionales
- ✅ Todas las validaciones solicitadas
- ✅ Diseño limpio y profesional
- ✅ Documentación completa
- ✅ Scripts de ayuda y pruebas
- ✅ Datos de ejemplo

**Para ejecutar inmediatamente:**

```bash
./compilar_idl.sh && python3 servidor.py
```

En otra terminal:
```bash
python3 cliente_admin.py
```

¡Listo para usar y demostrar! 🎬🍿

