# GUÍA DE USO DEL SISTEMA DE CINE

## Inicio Rápido

### 1. Compilar el IDL (primera vez)

```bash
./compilar_idl.sh
```

### 2. Verificar que todo está correcto

```bash
python3 test_corba.py
```

### 3. Iniciar el Servidor

**Opción A: Con servicio de nombres (recomendado)**

Terminal 1:
```bash
omniNames -start 2809
```

Terminal 2:
```bash
python3 servidor.py
```

**Opción B: Sin servicio de nombres**

```bash
python3 servidor.py
```

El servidor guardará su IOR en `servidor.ior` automáticamente.

### 4. Iniciar Cliente Administrador

Terminal 3:
```bash
python3 cliente_admin.py
```

### 5. Iniciar Cliente Usuario (opcional)

Terminal 4:
```bash
python3 cliente_usuario.py
```

---

## Flujo de Trabajo Típico

### Paso 1: Configuración Inicial (Administrador)

#### Crear Películas

1. En el cliente administrador, seleccionar: `1` (Gestión de Películas)
2. Seleccionar: `1` (Crear película)
3. Ingresar datos:
   ```
   Título: Avatar 2
   Género: Ciencia Ficción
   Duración (minutos): 180
   ```
4. Repetir para más películas

**Ejemplo de películas:**
- Avatar 2, Ciencia Ficción, 180 min
- Rápidos y Furiosos 10, Acción, 140 min
- The Batman, Acción, 175 min

#### Crear Salas

1. En el menú principal, seleccionar: `2` (Gestión de Salas)
2. Seleccionar: `1` (Crear sala)
3. Ingresar datos:
   ```
   Nombre de la sala: Sala VIP
   Número de filas (máx. 26): 8
   Número de columnas (máx. 20): 10
   ```

**Ejemplo de salas:**
- Sala VIP: 8 filas x 10 columnas (80 asientos)
- Sala Premium: 10 filas x 12 columnas (120 asientos)
- Sala Estándar: 12 filas x 15 columnas (180 asientos)

#### Crear Funciones

1. En el menú principal, seleccionar: `3` (Gestión de Funciones)
2. Seleccionar: `1` (Crear función)
3. El sistema mostrará las películas disponibles
4. Ingresar ID de película: `1`
5. El sistema mostrará las salas disponibles
6. Ingresar ID de sala: `1`
7. El sistema mostrará la semana actual y horario válido
8. Ingresar fecha (YYYY-MM-DD): `2026-03-02`
9. Ingresar hora (HH:MM): `18:00`

**Ejemplo de funciones:**
- Avatar 2, Sala VIP, 2026-03-02, 18:00
- Avatar 2, Sala VIP, 2026-03-02, 21:00
- Rápidos y Furiosos 10, Sala Premium, 2026-03-03, 16:00
- The Batman, Sala Estándar, 2026-03-03, 19:00

### Paso 2: Compra de Boletos

#### Opción A: Desde Cliente Administrador

1. Seleccionar: `4` (Generación de Boletos)
2. Ver funciones disponibles y seleccionar ID
3. Ver mapa de asientos
4. Ingresar nombre del cliente
5. Ingresar precio del boleto
6. Seleccionar asientos:
   ```
   Asiento: A5
   Asiento: A6
   Asiento: fin
   ```
7. El sistema mostrará los boletos generados

#### Opción B: Desde Cliente Usuario

1. Seleccionar: `3` (Comprar boletos)
2. Ver funciones disponibles
3. Seleccionar ID de función
4. Ver mapa de asientos
5. Ingresar nombre
6. Seleccionar asientos (ej: A5, A6)
7. Confirmar compra
8. Recibir boletos

---

## Validaciones Importantes

### Validación de Fechas

✅ **Permitido:**
- Fechas de la semana actual (lunes a domingo)
- Fecha de hoy o futuras

❌ **No permitido:**
- Fechas pasadas
- Fechas fuera de la semana actual

**Ejemplo:**
Si hoy es 2026-03-02 (lunes):
- ✅ 2026-03-02 a 2026-03-08 (semana actual)
- ❌ 2026-03-01 (pasado)
- ❌ 2026-03-09 (siguiente semana)

### Validación de Horarios

✅ **Permitido:**
- 08:00 a 23:00

❌ **No permitido:**
- Antes de 08:00
- Después de 23:00

### Validación de Asientos

✅ **Permitido:**
- Asientos disponibles (marcados con [ ])
- Formato: Letra + Número (ej: A5, B10, C1)

❌ **No permitido:**
- Asientos ocupados (marcados con [X])
- Filas fuera de rango (más allá de la última fila)
- Columnas fuera de rango (más allá de la última columna)

---

## Ejemplos de Uso Completos

### Ejemplo 1: Crear una función para hoy

```
1. Ir a Gestión de Funciones → Crear función
2. Seleccionar película: 1 (Avatar 2)
3. Seleccionar sala: 1 (Sala VIP)
4. Fecha: 2026-03-02 (hoy)
5. Hora: 18:00
6. ✓ Función creada exitosamente
```

### Ejemplo 2: Comprar 3 boletos

```
1. Ir a Comprar boletos (usuario) o Generación de Boletos (admin)
2. Seleccionar función: 1
3. Ver mapa de asientos:
   
        1  2  3  4  5  6  7  8  9 10
    A  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    B  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    C  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    ...

4. Nombre: Juan Pérez
5. Seleccionar asientos:
   - Asiento: C5
   - Asiento: C6
   - Asiento: C7
   - Asiento: fin

6. Confirmar compra
7. ✓ Recibir 3 boletos
```

### Ejemplo 3: Ver disponibilidad de una función

```
1. Cliente usuario → Ver funciones disponibles
2. Ver funciones por fecha: 2026-03-02
3. El sistema muestra:

   [1] 18:00 - Avatar 2
       Sala: Sala VIP
       Disponibles: 77/80 asientos
   
   [2] 21:00 - Avatar 2
       Sala: Sala VIP
       Disponibles: 80/80 asientos
```

### Ejemplo 4: Intentar crear función inválida

```
Fecha: 2026-02-28 (pasado)
✗ Error: No se pueden crear funciones en fechas pasadas

Fecha: 2026-03-15 (siguiente semana)
✗ Error: Las funciones solo pueden crearse en la semana actual

Hora: 07:00
✗ Error: La hora debe estar entre 08:00 y 23:00

Hora: 23:30
✗ Error: La hora debe estar entre 08:00 y 23:00
```

---

## Formato de Asientos

### Interpretación del Mapa

```
    1  2  3  4  5  6  7  8  9 10
A  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
B  [ ][ ][X][X][ ][ ][ ][ ][ ][ ]
C  [ ][ ][ ][ ][X][ ][ ][ ][ ][ ]
```

- **Fila A, Columna 1** → Ingresar: `A1`
- **Fila B, Columna 3** → `B3` (ocupado ❌)
- **Fila C, Columna 5** → `C5` (ocupado ❌)
- **Fila A, Columna 10** → `A10` (disponible ✓)

---

## Persistencia de Datos

El servidor guarda automáticamente:
- Películas
- Salas
- Funciones
- Boletos
- Estado de asientos

Los datos se guardan en: `datos_cine.json`

Al reiniciar el servidor, todos los datos se recuperan automáticamente.

---

## Comandos Útiles

### Ver estructura del proyecto
```bash
ls -la
```

### Limpiar datos (reiniciar sistema)
```bash
rm datos_cine.json
```

### Detener servidor
```
Ctrl + C
```

### Reiniciar servicio de nombres
```bash
killall omniNames
omniNames -start 2809
```

---

## Solución de Problemas

### Problema: "Cannot contact name service"

**Solución 1:** Iniciar servicio de nombres
```bash
omniNames -start 2809
```

**Solución 2:** El sistema usará IOR automáticamente

### Problema: "No se pudo conectar al servidor"

Verificar que el servidor esté corriendo:
```bash
ps aux | grep servidor.py
```

Si no está corriendo, iniciarlo:
```bash
python3 servidor.py
```

### Problema: Error al compilar IDL

Verificar que omniidl esté instalado:
```bash
which omniidl
```

Si no está instalado:
```bash
sudo apt-get install omniidl
```

---

## Preguntas Frecuentes

**P: ¿Puedo crear funciones para el próximo mes?**
R: No, solo se pueden crear funciones para la semana actual.

**P: ¿Qué pasa si intento reservar un asiento ocupado?**
R: El sistema mostrará un error y no permitirá la reserva.

**P: ¿Puedo cancelar un boleto?**
R: En la versión actual no hay cancelaciones. Los boletos son definitivos.

**P: ¿Cuántas salas puedo crear?**
R: Ilimitadas, pero cada sala tiene máximo 26 filas y 20 columnas.

**P: ¿Los datos se pierden al cerrar el servidor?**
R: No, todo se guarda en `datos_cine.json` y se recupera al reiniciar.

---

## Contacto y Soporte

Para reportar problemas o sugerencias, contactar al desarrollador.

Sistema desarrollado para el Primer Parcial de Sistemas Distribuidos.

