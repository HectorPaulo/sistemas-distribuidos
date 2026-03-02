# RESUMEN DEL PROYECTO

## Sistema de Cine con CORBA

### Descripción
Sistema completo de gestión de cine implementado con CORBA (Common Object Request Broker Architecture) en Python, cumpliendo con todos los requisitos solicitados.

---

## ✅ Requisitos Cumplidos

### 1. Apartados de Creación

✅ **Creación de Películas**
- Registro con título, género y duración
- Validación de datos
- Persistencia automática

✅ **Creación de Salas**
- Configuración de filas (máx. 26: A-Z)
- Configuración de columnas (máx. 20)
- Capacidad total automática

✅ **Generación de Funciones**
- Asignación de película y sala
- Programación con fecha y hora
- Control de conflictos

✅ **Generación de Boletos (lado administrador)**
- Creación individual o múltiple
- Validación de disponibilidad
- Diseño de boleto limpio

### 2. Validaciones Implementadas

✅ **Funciones solo en horario de actividades**
- Horario del cine: 08:00 - 23:00
- Validación automática al crear función

✅ **No crear funciones en fechas pasadas**
- Validación de fecha >= hoy
- Mensaje de error descriptivo

✅ **Funciones solo en la semana actual**
- Cálculo automático de semana
- Rango: lunes a domingo de la semana actual

✅ **Diseño de sala con filas y columnas**
- Visualización clara: [ ] disponible, [X] ocupado
- Identificación de filas: A, B, C, ...
- Identificación de columnas: 1, 2, 3, ...

✅ **Selección de asientos**
- Formato intuitivo: A5, B10, C3
- Validación de disponibilidad
- Prevención de doble reserva

✅ **Selección múltiple de asientos**
- Compra de varios boletos a la vez
- Diseño de boletos múltiples
- Rollback en caso de error

✅ **Diseño limpio**
- Sin degradados ni colores complejos
- Interfaz de texto clara y profesional
- Formato de boleto estructurado

---

## 📁 Estructura de Archivos

```
PrimerParcialSistemasDistribuidos/
│
├── cine.idl                    # Definición IDL de CORBA
├── cine_idl.py                 # Generado por omniidl
├── Cine/                       # Módulo generado
│   └── __init__.py
├── Cine__POA/                  # Módulo POA generado
│   └── __init__.py
│
├── servidor.py                 # Servidor CORBA
├── cliente_admin.py            # Cliente administrador
├── cliente_usuario.py          # Cliente usuario
│
├── compilar_idl.sh            # Script para compilar IDL
├── iniciar.sh                 # Script de inicio rápido
├── demo.sh                    # Script de demostración
├── test_corba.py              # Pruebas del sistema
├── crear_datos_ejemplo.py     # Crear datos de prueba
│
├── README.md                  # Documentación principal
├── GUIA_USO.md               # Guía de uso detallada
├── RESUMEN.md                # Este archivo
└── requirements.txt          # Dependencias Python
```

---

## 🚀 Inicio Rápido

### Opción 1: Demostración Automática

```bash
./demo.sh
```

Esto:
1. Compila el IDL (si es necesario)
2. Inicia el servidor
3. Crea datos de ejemplo
4. Deja el servidor corriendo

Luego abrir nuevas terminales para los clientes.

### Opción 2: Manual

```bash
# Terminal 1: Servidor
python3 servidor.py

# Terminal 2: Cliente Admin
python3 cliente_admin.py

# Terminal 3: Cliente Usuario
python3 cliente_usuario.py
```

### Opción 3: Datos de Ejemplo

```bash
# Iniciar servidor
python3 servidor.py

# En otra terminal, crear datos
python3 crear_datos_ejemplo.py
```

---

## 📊 Características Técnicas

### Arquitectura CORBA

- **IDL (Interface Definition Language)**: Define contratos
- **Servidor**: Implementa lógica de negocio
- **Clientes**: Consumen servicios remotos
- **ORB**: Gestiona comunicación distribuida

### Persistencia

- Formato: JSON (`datos_cine.json`)
- Guardado automático en cada operación
- Carga automática al iniciar servidor

### Estructuras de Datos

```idl
struct Pelicula {
    long id;
    string titulo;
    string genero;
    long duracion;
};

struct Sala {
    long id;
    string nombre;
    long filas;
    long columnas;
};

struct Funcion {
    long id;
    long peliculaId;
    long salaId;
    string fecha;
    string hora;
};

struct Boleto {
    long id;
    long funcionId;
    long fila;
    long columna;
    string nombreCliente;
    double precio;
};
```

### Validaciones

```python
# Fecha
- >= fecha actual
- dentro de semana actual (lun-dom)

# Hora
- >= 08:00
- <= 23:00

# Asientos
- fila: 0 a (filas-1)
- columna: 0 a (columnas-1)
- no ocupado

# Sala
- filas: 1 a 26
- columnas: 1 a 20
```

---

## 🎯 Casos de Uso

### Administrador

1. **Configurar cine**
   - Crear películas en cartelera
   - Definir salas disponibles
   - Programar funciones de la semana

2. **Generar boletos**
   - Ventas directas en taquilla
   - Reservas grupales
   - Ver estadísticas

### Usuario

1. **Consultar cartelera**
   - Ver películas disponibles
   - Filtrar por género
   - Ver duración

2. **Comprar boletos**
   - Seleccionar función
   - Ver mapa de asientos
   - Elegir ubicación
   - Confirmar compra

---

## 📋 Ejemplo de Flujo Completo

### 1. Administrador configura el cine

```
1. Crear película: "Avatar 2", Ciencia Ficción, 192 min
2. Crear sala: "Sala VIP", 8 filas, 10 columnas
3. Crear función: Avatar 2, Sala VIP, 2026-03-02, 18:00
```

### 2. Usuario compra boletos

```
1. Ver funciones disponibles
2. Seleccionar función ID 1
3. Ver mapa de asientos:
   
        1  2  3  4  5  6  7  8  9 10
    A  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    B  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    C  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]

4. Seleccionar asientos: C5, C6
5. Confirmar compra
6. Recibir boletos
```

### 3. Resultado

```
============================================================
BOLETOS
============================================================
Cliente: Juan Pérez
------------------------------------------------------------
Película: Avatar 2
Género: Ciencia Ficción
Duración: 192 minutos
------------------------------------------------------------
Sala: Sala VIP
Fecha: 2026-03-02
Hora: 18:00
------------------------------------------------------------
Asientos:
  Boleto #1 - C5 - $50.00
  Boleto #2 - C6 - $50.00
------------------------------------------------------------
Cantidad de boletos: 2
Total: $100.00
============================================================
```

---

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje principal
- **omniORB**: Implementación CORBA
- **omniORBpy**: Bindings Python para CORBA
- **IDL**: Definición de interfaces
- **JSON**: Persistencia de datos

---

## 📝 Validaciones de Negocio

### ✅ Validaciones Implementadas

| Validación | Descripción | Mensaje de Error |
|------------|-------------|------------------|
| Fecha pasada | No permite fechas anteriores a hoy | "No se pueden crear funciones en fechas pasadas" |
| Semana actual | Solo permite fechas de lun-dom actual | "Las funciones solo pueden crearse en la semana actual" |
| Horario | 08:00 - 23:00 | "La hora debe estar entre 08:00 y 23:00" |
| Asiento ocupado | Verifica disponibilidad | "El asiento ya está ocupado" |
| Conflicto sala | Previene doble programación | "Ya existe una función en esta sala, fecha y hora" |

---

## 🎨 Diseño de Interfaz

### Principios de Diseño

✅ **Limpieza**
- Sin colores complejos
- Sin efectos visuales
- Texto plano y claro

✅ **Claridad**
- Separadores visuales (=, -)
- Espaciado apropiado
- Mensajes descriptivos

✅ **Consistencia**
- Formato uniforme en boletos
- Símbolos consistentes (✓, ✗, ⚠)
- Estructura predecible

### Ejemplo de Mapa de Asientos

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
 E   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]

------------------------------------------------------------
PANTALLA
============================================================
```

---

## 📚 Documentación Disponible

1. **README.md** - Documentación completa del proyecto
2. **GUIA_USO.md** - Guía detallada con ejemplos
3. **RESUMEN.md** - Este archivo (resumen ejecutivo)

---

## 🔧 Mantenimiento

### Reiniciar el sistema

```bash
# Detener servidor (Ctrl+C)
# Borrar datos
rm datos_cine.json

# Reiniciar servidor
python3 servidor.py
```

### Ver logs

El servidor imprime en consola:
- Operaciones realizadas
- Errores de validación
- Conexiones de clientes

### Backup de datos

```bash
# Copiar archivo de datos
cp datos_cine.json datos_cine_backup.json

# Restaurar
cp datos_cine_backup.json datos_cine.json
```

---

## 🎓 Notas Académicas

### Cumplimiento de Requisitos

Este proyecto cumple 100% con los requisitos del Primer Parcial:

1. ✅ Usa CORBA como tecnología de sistemas distribuidos
2. ✅ Implementa todas las funcionalidades solicitadas
3. ✅ Incluye todas las validaciones requeridas
4. ✅ Diseño limpio sin efectos visuales complejos
5. ✅ Separación cliente-servidor
6. ✅ Persistencia de datos
7. ✅ Manejo de errores robusto

### Conceptos Demostrados

- **Sistemas Distribuidos**: Cliente-servidor con CORBA
- **IDL**: Definición de interfaces independiente del lenguaje
- **RPC**: Llamadas a procedimientos remotos
- **Persistencia**: Almacenamiento de estado
- **Validación**: Reglas de negocio
- **Manejo de Errores**: Excepciones CORBA

---

## 📞 Soporte

Para problemas comunes, consultar:
- README.md - Sección "Problemas Comunes"
- GUIA_USO.md - Sección "Solución de Problemas"

---

## 📄 Licencia

Proyecto académico para Sistemas Distribuidos.

---

**Fecha de entrega**: 2026-03-02  
**Asignatura**: Sistemas Distribuidos  
**Tema**: Primer Parcial - Sistema de Cine con CORBA

