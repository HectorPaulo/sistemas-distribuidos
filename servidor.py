#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime, timedelta
from omniORB import CORBA
import CosNaming
import Cine, Cine__POA


class SistemaCineImpl(Cine__POA.SistemaCine):
    """Implementación del servidor del sistema de cine"""

    def __init__(self):
        self.peliculas = {}
        self.salas = {}
        self.funciones = {}
        self.boletos = {}
        self.asientos_ocupados = {}  # {funcionId: [(fila, columna), ...]}

        self.siguiente_id_pelicula = 1
        self.siguiente_id_sala = 1
        self.siguiente_id_funcion = 1
        self.siguiente_id_boleto = 1

        # Horarios del cine
        self.hora_apertura = "08:00"
        self.hora_cierre = "23:00"

        self._cargar_datos()

    def _cargar_datos(self):
        """Cargar datos desde archivos si existen"""
        if os.path.exists('datos_cine.json'):
            try:
                with open('datos_cine.json', 'r') as f:
                    datos = json.load(f)
                    self.peliculas = {int(k): v for k, v in datos.get('peliculas', {}).items()}
                    self.salas = {int(k): v for k, v in datos.get('salas', {}).items()}
                    self.funciones = {int(k): v for k, v in datos.get('funciones', {}).items()}
                    self.boletos = {int(k): v for k, v in datos.get('boletos', {}).items()}
                    self.asientos_ocupados = {int(k): [tuple(a) for a in v]
                                             for k, v in datos.get('asientos_ocupados', {}).items()}

                    self.siguiente_id_pelicula = datos.get('siguiente_id_pelicula', 1)
                    self.siguiente_id_sala = datos.get('siguiente_id_sala', 1)
                    self.siguiente_id_funcion = datos.get('siguiente_id_funcion', 1)
                    self.siguiente_id_boleto = datos.get('siguiente_id_boleto', 1)

                print("Datos cargados correctamente.")
            except Exception as e:
                print(f"Error al cargar datos: {e}")

    def _guardar_datos(self):
        """Guardar datos en archivo"""
        try:
            datos = {
                'peliculas': self.peliculas,
                'salas': self.salas,
                'funciones': self.funciones,
                'boletos': self.boletos,
                'asientos_ocupados': {k: list(v) for k, v in self.asientos_ocupados.items()},
                'siguiente_id_pelicula': self.siguiente_id_pelicula,
                'siguiente_id_sala': self.siguiente_id_sala,
                'siguiente_id_funcion': self.siguiente_id_funcion,
                'siguiente_id_boleto': self.siguiente_id_boleto
            }
            with open('datos_cine.json', 'w') as f:
                json.dump(datos, f, indent=2)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def _validar_fecha(self, fecha_str):
        """Valida que la fecha sea válida y no sea anterior a hoy"""
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            hoy = datetime.now().date()

            if fecha < hoy:
                raise Cine.ErrorValidacion(
                    "No se pueden crear funciones en fechas pasadas"
                )

            # Validar que la fecha esté dentro de la semana actual
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)

            if fecha < inicio_semana or fecha > fin_semana:
                raise Cine.ErrorValidacion(
                    f"Las funciones solo pueden crearse en la semana actual "
                    f"({inicio_semana.strftime('%Y-%m-%d')} a {fin_semana.strftime('%Y-%m-%d')})"
                )

            return fecha
        except ValueError:
            raise Cine.ErrorValidacion(
                "Formato de fecha inválido. Use YYYY-MM-DD"
            )

    def _validar_hora(self, hora_str):
        """Valida que la hora esté dentro del horario del cine"""
        try:
            hora = datetime.strptime(hora_str, "%H:%M").time()
            apertura = datetime.strptime(self.hora_apertura, "%H:%M").time()
            cierre = datetime.strptime(self.hora_cierre, "%H:%M").time()

            if hora < apertura or hora > cierre:
                raise Cine.ErrorValidacion(
                    f"La hora debe estar entre {self.hora_apertura} y {self.hora_cierre}"
                )

            return hora
        except ValueError:
            raise Cine.ErrorValidacion(
                "Formato de hora inválido. Use HH:MM"
            )

    # ========== Gestión de Películas ==========

    def crearPelicula(self, titulo, genero, duracion):
        """Crear una nueva película"""
        if not titulo or not titulo.strip():
            raise Cine.ErrorValidacion("El título no puede estar vacío")

        if duracion <= 0:
            raise Cine.ErrorValidacion("La duración debe ser mayor a 0")

        id_pelicula = self.siguiente_id_pelicula
        self.peliculas[id_pelicula] = {
            'id': id_pelicula,
            'titulo': titulo,
            'genero': genero,
            'duracion': duracion
        }
        self.siguiente_id_pelicula += 1
        self._guardar_datos()

        print(f"Película creada: {titulo} (ID: {id_pelicula})")
        return id_pelicula

    def obtenerPeliculas(self):
        """Obtener lista de todas las películas"""
        peliculas = []
        for p in self.peliculas.values():
            pelicula = Cine.Pelicula(
                p['id'], p['titulo'], p['genero'], p['duracion']
            )
            peliculas.append(pelicula)
        return peliculas

    def obtenerPelicula(self, id):
        """Obtener una película por ID"""
        if id not in self.peliculas:
            raise Cine.ErrorValidacion(f"Película con ID {id} no encontrada")

        p = self.peliculas[id]
        return Cine.Pelicula(p['id'], p['titulo'], p['genero'], p['duracion'])

    # ========== Gestión de Salas ==========

    def crearSala(self, nombre, filas, columnas):
        """Crear una nueva sala"""
        if not nombre or not nombre.strip():
            raise Cine.ErrorValidacion("El nombre de la sala no puede estar vacío")

        if filas <= 0 or columnas <= 0:
            raise Cine.ErrorValidacion("Filas y columnas deben ser mayores a 0")

        if filas > 26:
            raise Cine.ErrorValidacion("Máximo 26 filas permitidas (A-Z)")

        if columnas > 20:
            raise Cine.ErrorValidacion("Máximo 20 columnas permitidas")

        id_sala = self.siguiente_id_sala
        self.salas[id_sala] = {
            'id': id_sala,
            'nombre': nombre,
            'filas': filas,
            'columnas': columnas
        }
        self.siguiente_id_sala += 1
        self._guardar_datos()

        print(f"Sala creada: {nombre} (ID: {id_sala}, {filas}x{columnas})")
        return id_sala

    def obtenerSalas(self):
        """Obtener lista de todas las salas"""
        salas = []
        for s in self.salas.values():
            sala = Cine.Sala(s['id'], s['nombre'], s['filas'], s['columnas'])
            salas.append(sala)
        return salas

    def obtenerSala(self, id):
        """Obtener una sala por ID"""
        if id not in self.salas:
            raise Cine.ErrorValidacion(f"Sala con ID {id} no encontrada")

        s = self.salas[id]
        return Cine.Sala(s['id'], s['nombre'], s['filas'], s['columnas'])

    # ========== Gestión de Funciones ==========

    def crearFuncion(self, peliculaId, salaId, fecha, hora):
        """Crear una nueva función"""
        if peliculaId not in self.peliculas:
            raise Cine.ErrorValidacion(f"Película con ID {peliculaId} no encontrada")

        if salaId not in self.salas:
            raise Cine.ErrorValidacion(f"Sala con ID {salaId} no encontrada")

        # Validar fecha y hora
        self._validar_fecha(fecha)
        self._validar_hora(hora)

        # Verificar que no haya otra función en la misma sala, fecha y hora
        for f in self.funciones.values():
            if (f['salaId'] == salaId and f['fecha'] == fecha and
                f['hora'] == hora):
                raise Cine.ErrorValidacion(
                    "Ya existe una función en esta sala, fecha y hora"
                )

        id_funcion = self.siguiente_id_funcion
        self.funciones[id_funcion] = {
            'id': id_funcion,
            'peliculaId': peliculaId,
            'salaId': salaId,
            'fecha': fecha,
            'hora': hora
        }
        self.asientos_ocupados[id_funcion] = []
        self.siguiente_id_funcion += 1
        self._guardar_datos()

        print(f"Función creada (ID: {id_funcion}) - {fecha} {hora}")
        return id_funcion

    def obtenerFunciones(self):
        """Obtener lista de todas las funciones"""
        funciones = []
        for f in self.funciones.values():
            funcion = Cine.Funcion(
                f['id'], f['peliculaId'], f['salaId'], f['fecha'], f['hora']
            )
            funciones.append(funcion)
        return funciones

    def obtenerFuncionesPorFecha(self, fecha):
        """Obtener funciones de una fecha específica"""
        funciones = []
        for f in self.funciones.values():
            if f['fecha'] == fecha:
                funcion = Cine.Funcion(
                    f['id'], f['peliculaId'], f['salaId'], f['fecha'], f['hora']
                )
                funciones.append(funcion)
        return funciones

    def obtenerFuncion(self, id):
        """Obtener una función por ID"""
        if id not in self.funciones:
            raise Cine.ErrorValidacion(f"Función con ID {id} no encontrada")

        f = self.funciones[id]
        return Cine.Funcion(f['id'], f['peliculaId'], f['salaId'],
                           f['fecha'], f['hora'])

    # ========== Gestión de Asientos y Boletos ==========

    def obtenerAsientosFuncion(self, funcionId):
        """Obtener el estado de todos los asientos de una función"""
        if funcionId not in self.funciones:
            raise Cine.ErrorValidacion(f"Función con ID {funcionId} no encontrada")

        funcion = self.funciones[funcionId]
        sala = self.salas[funcion['salaId']]
        ocupados = self.asientos_ocupados.get(funcionId, [])

        asientos = []
        for fila in range(sala['filas']):
            for columna in range(sala['columnas']):
                ocupado = (fila, columna) in ocupados
                asiento = Cine.Asiento(fila, columna, ocupado)
                asientos.append(asiento)

        return asientos

    def generarBoleto(self, funcionId, fila, columna, nombreCliente, precio):
        """Generar un boleto individual"""
        if funcionId not in self.funciones:
            raise Cine.ErrorValidacion(f"Función con ID {funcionId} no encontrada")

        funcion = self.funciones[funcionId]
        sala = self.salas[funcion['salaId']]

        # Validar asiento
        if fila < 0 or fila >= sala['filas']:
            raise Cine.ErrorValidacion("Fila inválida")

        if columna < 0 or columna >= sala['columnas']:
            raise Cine.ErrorValidacion("Columna inválida")

        # Verificar disponibilidad
        if funcionId not in self.asientos_ocupados:
            self.asientos_ocupados[funcionId] = []

        if (fila, columna) in self.asientos_ocupados[funcionId]:
            raise Cine.ErrorValidacion("El asiento ya está ocupado")

        # Crear boleto
        id_boleto = self.siguiente_id_boleto
        self.boletos[id_boleto] = {
            'id': id_boleto,
            'funcionId': funcionId,
            'fila': fila,
            'columna': columna,
            'nombreCliente': nombreCliente,
            'precio': precio
        }

        self.asientos_ocupados[funcionId].append((fila, columna))
        self.siguiente_id_boleto += 1
        self._guardar_datos()

        print(f"Boleto generado (ID: {id_boleto}) para {nombreCliente}")
        return id_boleto

    def generarBoletosMultiples(self, funcionId, filas, columnas,
                               nombreCliente, precio):
        """Generar múltiples boletos"""
        if len(filas) != len(columnas):
            raise Cine.ErrorValidacion(
                "Las listas de filas y columnas deben tener la misma longitud"
            )

        boletos = []
        ids_creados = []

        try:
            for i in range(len(filas)):
                id_boleto = self.generarBoleto(
                    funcionId, filas[i], columnas[i], nombreCliente, precio
                )
                ids_creados.append(id_boleto)
        except Cine.ErrorValidacion as e:
            # Revertir boletos creados si hay error
            for id_boleto in ids_creados:
                if id_boleto in self.boletos:
                    b = self.boletos[id_boleto]
                    self.asientos_ocupados[funcionId].remove((b['fila'], b['columna']))
                    del self.boletos[id_boleto]
            self._guardar_datos()
            raise e

        # Obtener boletos creados
        for id_boleto in ids_creados:
            b = self.boletos[id_boleto]
            boleto = Cine.Boleto(
                b['id'], b['funcionId'], b['fila'], b['columna'],
                b['nombreCliente'], b['precio']
            )
            boletos.append(boleto)

        return boletos

    def obtenerBoleto(self, id):
        """Obtener un boleto por ID"""
        if id not in self.boletos:
            raise Cine.ErrorValidacion(f"Boleto con ID {id} no encontrado")

        b = self.boletos[id]
        return Cine.Boleto(b['id'], b['funcionId'], b['fila'], b['columna'],
                          b['nombreCliente'], b['precio'])

    def obtenerTodosBoletos(self):
        """Obtener todos los boletos"""
        boletos = []
        for b in self.boletos.values():
            boleto = Cine.Boleto(
                b['id'], b['funcionId'], b['fila'], b['columna'],
                b['nombreCliente'], b['precio']
            )
            boletos.append(boleto)
        return boletos


def main():
    """Iniciar servidor CORBA"""
    try:
        # Inicializar ORB
        orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

        # Obtener POA
        poa = orb.resolve_initial_references("RootPOA")
        poa._get_the_POAManager().activate()

        # Crear objeto servidor
        servidor = SistemaCineImpl()

        # Activar objeto en POA
        poa.activate_object(servidor)

        # Obtener referencia del objeto
        obj_ref = servidor._this()

        # Registrar en el servicio de nombres
        try:
            naming_context = orb.resolve_initial_references("NameService")
            naming_context = naming_context._narrow(CosNaming.NamingContext)

            name = [CosNaming.NameComponent("SistemaCine", "Object")]

            try:
                naming_context.unbind(name)
            except:
                pass

            naming_context.bind(name, obj_ref)
            print("Servidor registrado en el servicio de nombres como 'SistemaCine'")
        except Exception as e:
            print(f"No se pudo registrar en el servicio de nombres: {e}")
            print("Guardando IOR en archivo...")

            # Guardar IOR en archivo como alternativa
            ior = orb.object_to_string(obj_ref)
            with open("servidor.ior", "w") as f:
                f.write(ior)
            print("IOR guardado en 'servidor.ior'")

        print("Servidor de Cine iniciado y esperando solicitudes...")
        print(f"Horario de operación: {servidor.hora_apertura} - {servidor.hora_cierre}")
        print("Presione Ctrl+C para detener el servidor")

        # Ejecutar servidor
        orb.run()

    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error en el servidor: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

