#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta
from omniORB import CORBA
import CosNaming
import Cine


class ClienteAdministrador:
    """Cliente para funciones administrativas del cine"""

    def __init__(self):
        self.sistema = None
        self.conectar()

    def conectar(self):
        """Conectar al servidor CORBA"""
        try:
            orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

            try:
                # Intentar conectar usando servicio de nombres
                naming_context = orb.resolve_initial_references("NameService")
                naming_context = naming_context._narrow(CosNaming.NamingContext)
                name = [CosNaming.NameComponent("SistemaCine", "Object")]
                obj = naming_context.resolve(name)
                self.sistema = obj._narrow(Cine.SistemaCine)
            except:
                # Si falla, usar IOR desde archivo
                with open("servidor.ior", "r") as f:
                    ior = f.read()
                obj = orb.string_to_object(ior)
                self.sistema = obj._narrow(Cine.SistemaCine)

            if self.sistema is None:
                raise Exception("No se pudo conectar al servidor")

            print("=" * 60)
            print("CLIENTE ADMINISTRADOR - SISTEMA DE CINE")
            print("=" * 60)
            print("Conectado al servidor correctamente\n")

        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            sys.exit(1)

    def limpiar_pantalla(self):
        """Limpiar la pantalla"""
        print("\n" * 2)

    def mostrar_menu_principal(self):
        """Mostrar menú principal"""
        print("\n" + "=" * 60)
        print("MENU ADMINISTRADOR")
        print("=" * 60)
        print("1. Gestión de Películas")
        print("2. Gestión de Salas")
        print("3. Gestión de Funciones")
        print("4. Generación de Boletos")
        print("5. Ver Todos los Boletos")
        print("0. Salir")
        print("=" * 60)

    # ========== Gestión de Películas ==========

    def menu_peliculas(self):
        """Menú de gestión de películas"""
        while True:
            print("\n" + "-" * 60)
            print("GESTION DE PELICULAS")
            print("-" * 60)
            print("1. Crear película")
            print("2. Listar películas")
            print("0. Volver")
            print("-" * 60)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_pelicula()
            elif opcion == "2":
                self.listar_peliculas()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")

    def crear_pelicula(self):
        """Crear una nueva película"""
        print("\n" + "-" * 60)
        print("CREAR PELICULA")
        print("-" * 60)

        try:
            titulo = input("Título: ").strip()
            genero = input("Género: ").strip()
            duracion = int(input("Duración (minutos): ").strip())

            id_pelicula = self.sistema.crearPelicula(titulo, genero, duracion)
            print(f"\n✓ Película creada exitosamente (ID: {id_pelicula})")

        except Cine.ErrorValidacion as e:
            print(f"\n✗ Error: {e.mensaje}")
        except ValueError:
            print("\n✗ Error: La duración debe ser un número entero")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")

    def listar_peliculas(self):
        """Listar todas las películas"""
        print("\n" + "-" * 60)
        print("LISTA DE PELICULAS")
        print("-" * 60)

        try:
            peliculas = self.sistema.obtenerPeliculas()

            if not peliculas:
                print("No hay películas registradas")
                return

            for p in peliculas:
                print(f"\nID: {p.id}")
                print(f"  Título: {p.titulo}")
                print(f"  Género: {p.genero}")
                print(f"  Duración: {p.duracion} minutos")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    # ========== Gestión de Salas ==========

    def menu_salas(self):
        """Menú de gestión de salas"""
        while True:
            print("\n" + "-" * 60)
            print("GESTION DE SALAS")
            print("-" * 60)
            print("1. Crear sala")
            print("2. Listar salas")
            print("0. Volver")
            print("-" * 60)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_sala()
            elif opcion == "2":
                self.listar_salas()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")

    def crear_sala(self):
        """Crear una nueva sala"""
        print("\n" + "-" * 60)
        print("CREAR SALA")
        print("-" * 60)

        try:
            nombre = input("Nombre de la sala: ").strip()
            filas = int(input("Número de filas (máx. 26): ").strip())
            columnas = int(input("Número de columnas (máx. 20): ").strip())

            id_sala = self.sistema.crearSala(nombre, filas, columnas)
            print(f"\n✓ Sala creada exitosamente (ID: {id_sala})")

        except Cine.ErrorValidacion as e:
            print(f"\n✗ Error: {e.mensaje}")
        except ValueError:
            print("\n✗ Error: Filas y columnas deben ser números enteros")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")

    def listar_salas(self):
        """Listar todas las salas"""
        print("\n" + "-" * 60)
        print("LISTA DE SALAS")
        print("-" * 60)

        try:
            salas = self.sistema.obtenerSalas()

            if not salas:
                print("No hay salas registradas")
                return

            for s in salas:
                print(f"\nID: {s.id}")
                print(f"  Nombre: {s.nombre}")
                print(f"  Capacidad: {s.filas} filas x {s.columnas} columnas")
                print(f"  Total asientos: {s.filas * s.columnas}")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    # ========== Gestión de Funciones ==========

    def menu_funciones(self):
        """Menú de gestión de funciones"""
        while True:
            print("\n" + "-" * 60)
            print("GESTION DE FUNCIONES")
            print("-" * 60)
            print("1. Crear función")
            print("2. Listar todas las funciones")
            print("3. Listar funciones por fecha")
            print("0. Volver")
            print("-" * 60)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_funcion()
            elif opcion == "2":
                self.listar_funciones()
            elif opcion == "3":
                self.listar_funciones_por_fecha()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")

    def crear_funcion(self):
        """Crear una nueva función"""
        print("\n" + "-" * 60)
        print("CREAR FUNCION")
        print("-" * 60)

        try:
            # Mostrar películas disponibles
            peliculas = self.sistema.obtenerPeliculas()
            if not peliculas:
                print("No hay películas registradas. Cree una película primero.")
                return

            print("\nPelículas disponibles:")
            for p in peliculas:
                print(f"  {p.id}. {p.titulo} ({p.duracion} min)")

            pelicula_id = int(input("\nID de la película: ").strip())

            # Mostrar salas disponibles
            salas = self.sistema.obtenerSalas()
            if not salas:
                print("No hay salas registradas. Cree una sala primero.")
                return

            print("\nSalas disponibles:")
            for s in salas:
                print(f"  {s.id}. {s.nombre} ({s.filas}x{s.columnas})")

            sala_id = int(input("\nID de la sala: ").strip())

            # Mostrar información de validación
            hoy = datetime.now().date()
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)

            print(f"\nSemana actual: {inicio_semana.strftime('%Y-%m-%d')} "
                  f"a {fin_semana.strftime('%Y-%m-%d')}")
            print("Horario: 08:00 a 23:00")

            fecha = input("\nFecha (YYYY-MM-DD): ").strip()
            hora = input("Hora (HH:MM): ").strip()

            id_funcion = self.sistema.crearFuncion(pelicula_id, sala_id,
                                                  fecha, hora)
            print(f"\n✓ Función creada exitosamente (ID: {id_funcion})")

        except Cine.ErrorValidacion as e:
            print(f"\n✗ Error: {e.mensaje}")
        except ValueError:
            print("\n✗ Error: ID debe ser un número entero")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")

    def listar_funciones(self):
        """Listar todas las funciones"""
        print("\n" + "-" * 60)
        print("LISTA DE FUNCIONES")
        print("-" * 60)

        try:
            funciones = self.sistema.obtenerFunciones()

            if not funciones:
                print("No hay funciones registradas")
                return

            for f in funciones:
                pelicula = self.sistema.obtenerPelicula(f.peliculaId)
                sala = self.sistema.obtenerSala(f.salaId)

                print(f"\nID: {f.id}")
                print(f"  Película: {pelicula.titulo}")
                print(f"  Sala: {sala.nombre}")
                print(f"  Fecha: {f.fecha}")
                print(f"  Hora: {f.hora}")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    def listar_funciones_por_fecha(self):
        """Listar funciones de una fecha específica"""
        print("\n" + "-" * 60)
        print("FUNCIONES POR FECHA")
        print("-" * 60)

        try:
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            funciones = self.sistema.obtenerFuncionesPorFecha(fecha)

            if not funciones:
                print(f"No hay funciones para la fecha {fecha}")
                return

            for f in funciones:
                pelicula = self.sistema.obtenerPelicula(f.peliculaId)
                sala = self.sistema.obtenerSala(f.salaId)

                print(f"\nID: {f.id}")
                print(f"  Película: {pelicula.titulo}")
                print(f"  Sala: {sala.nombre}")
                print(f"  Hora: {f.hora}")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    # ========== Generación de Boletos ==========

    def menu_generar_boletos(self):
        """Menú para generar boletos"""
        print("\n" + "-" * 60)
        print("GENERACION DE BOLETOS")
        print("-" * 60)

        try:
            # Listar funciones disponibles
            funciones = self.sistema.obtenerFunciones()
            if not funciones:
                print("No hay funciones disponibles")
                return

            print("\nFunciones disponibles:")
            for f in funciones:
                pelicula = self.sistema.obtenerPelicula(f.peliculaId)
                sala = self.sistema.obtenerSala(f.salaId)
                print(f"\n  {f.id}. {pelicula.titulo}")
                print(f"     Sala: {sala.nombre} | Fecha: {f.fecha} | Hora: {f.hora}")

            funcion_id = int(input("\nID de la función: ").strip())

            # Obtener información de la función
            funcion = self.sistema.obtenerFuncion(funcion_id)
            sala = self.sistema.obtenerSala(funcion.salaId)
            pelicula = self.sistema.obtenerPelicula(funcion.peliculaId)

            # Mostrar mapa de asientos
            self.mostrar_mapa_asientos(funcion_id)

            # Solicitar información del cliente
            nombre_cliente = input("\nNombre del cliente: ").strip()
            precio = float(input("Precio del boleto: $").strip())

            print("\nIngrese los asientos a reservar (ej: A5, B10)")
            print("Escriba 'fin' cuando termine")

            asientos = []
            while True:
                asiento = input("Asiento: ").strip().upper()
                if asiento == 'FIN':
                    break

                try:
                    # Convertir formato A5 a fila,columna
                    fila_letra = asiento[0]
                    columna_num = int(asiento[1:])

                    fila = ord(fila_letra) - ord('A')
                    columna = columna_num - 1

                    if fila < 0 or fila >= sala.filas:
                        print(f"✗ Fila inválida (debe ser A-{chr(ord('A')+sala.filas-1)})")
                        continue

                    if columna < 0 or columna >= sala.columnas:
                        print(f"✗ Columna inválida (debe ser 1-{sala.columnas})")
                        continue

                    asientos.append((fila, columna))
                    print(f"✓ Asiento {asiento} agregado")

                except (ValueError, IndexError):
                    print("✗ Formato inválido. Use formato como A5, B10, etc.")

            if not asientos:
                print("No se seleccionaron asientos")
                return

            # Generar boletos
            if len(asientos) == 1:
                id_boleto = self.sistema.generarBoleto(
                    funcion_id, asientos[0][0], asientos[0][1],
                    nombre_cliente, precio
                )
                self.mostrar_boleto(id_boleto)
            else:
                filas = [a[0] for a in asientos]
                columnas = [a[1] for a in asientos]
                boletos = self.sistema.generarBoletosMultiples(
                    funcion_id, filas, columnas, nombre_cliente, precio
                )
                self.mostrar_boletos_multiples(boletos)

        except Cine.ErrorValidacion as e:
            print(f"\n✗ Error: {e.mensaje}")
        except ValueError:
            print("\n✗ Error: Valor numérico inválido")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")

    def mostrar_mapa_asientos(self, funcion_id):
        """Mostrar el mapa de asientos de una función"""
        try:
            funcion = self.sistema.obtenerFuncion(funcion_id)
            sala = self.sistema.obtenerSala(funcion.salaId)
            asientos = self.sistema.obtenerAsientosFuncion(funcion_id)

            print("\n" + "=" * 60)
            print("MAPA DE ASIENTOS")
            print("=" * 60)
            print("[ ] = Disponible    [X] = Ocupado")
            print("-" * 60)

            # Encabezado de columnas
            print("    ", end="")
            for col in range(sala.columnas):
                print(f"{col+1:3d}", end="")
            print()

            # Filas con asientos
            for fila in range(sala.filas):
                fila_letra = chr(ord('A') + fila)
                print(f" {fila_letra}  ", end="")

                for col in range(sala.columnas):
                    # Buscar asiento en la lista
                    ocupado = False
                    for asiento in asientos:
                        if asiento.fila == fila and asiento.columna == col:
                            ocupado = asiento.ocupado
                            break

                    if ocupado:
                        print(" [X]", end="")
                    else:
                        print(" [ ]", end="")

                print()

            print("=" * 60)

        except Exception as e:
            print(f"Error al mostrar mapa de asientos: {e}")

    def mostrar_boleto(self, id_boleto):
        """Mostrar un boleto individual"""
        try:
            boleto = self.sistema.obtenerBoleto(id_boleto)
            funcion = self.sistema.obtenerFuncion(boleto.funcionId)
            pelicula = self.sistema.obtenerPelicula(funcion.peliculaId)
            sala = self.sistema.obtenerSala(funcion.salaId)

            fila_letra = chr(ord('A') + boleto.fila)
            columna_num = boleto.columna + 1

            print("\n" + "=" * 60)
            print("BOLETO GENERADO")
            print("=" * 60)
            print(f"Boleto #: {boleto.id}")
            print(f"Cliente: {boleto.nombreCliente}")
            print("-" * 60)
            print(f"Película: {pelicula.titulo}")
            print(f"Sala: {sala.nombre}")
            print(f"Fecha: {funcion.fecha}")
            print(f"Hora: {funcion.hora}")
            print(f"Asiento: {fila_letra}{columna_num}")
            print(f"Precio: ${boleto.precio:.2f}")
            print("=" * 60)

        except Exception as e:
            print(f"Error al mostrar boleto: {e}")

    def mostrar_boletos_multiples(self, boletos):
        """Mostrar múltiples boletos"""
        if not boletos:
            return

        try:
            # Obtener información común
            primer_boleto = boletos[0]
            funcion = self.sistema.obtenerFuncion(primer_boleto.funcionId)
            pelicula = self.sistema.obtenerPelicula(funcion.peliculaId)
            sala = self.sistema.obtenerSala(funcion.salaId)

            total = sum(b.precio for b in boletos)

            print("\n" + "=" * 60)
            print("BOLETOS GENERADOS")
            print("=" * 60)
            print(f"Cliente: {primer_boleto.nombreCliente}")
            print(f"Película: {pelicula.titulo}")
            print(f"Sala: {sala.nombre}")
            print(f"Fecha: {funcion.fecha} | Hora: {funcion.hora}")
            print("-" * 60)

            for boleto in boletos:
                fila_letra = chr(ord('A') + boleto.fila)
                columna_num = boleto.columna + 1
                print(f"Boleto #{boleto.id} - Asiento: {fila_letra}{columna_num} "
                      f"- Precio: ${boleto.precio:.2f}")

            print("-" * 60)
            print(f"Total: ${total:.2f}")
            print(f"Cantidad de boletos: {len(boletos)}")
            print("=" * 60)

        except Exception as e:
            print(f"Error al mostrar boletos: {e}")

    def listar_todos_boletos(self):
        """Listar todos los boletos generados"""
        print("\n" + "-" * 60)
        print("TODOS LOS BOLETOS")
        print("-" * 60)

        try:
            boletos = self.sistema.obtenerTodosBoletos()

            if not boletos:
                print("No hay boletos generados")
                return

            for boleto in boletos:
                funcion = self.sistema.obtenerFuncion(boleto.funcionId)
                pelicula = self.sistema.obtenerPelicula(funcion.peliculaId)
                sala = self.sistema.obtenerSala(funcion.salaId)

                fila_letra = chr(ord('A') + boleto.fila)
                columna_num = boleto.columna + 1

                print(f"\nBoleto #{boleto.id}")
                print(f"  Cliente: {boleto.nombreCliente}")
                print(f"  Película: {pelicula.titulo}")
                print(f"  Sala: {sala.nombre}")
                print(f"  Fecha: {funcion.fecha} | Hora: {funcion.hora}")
                print(f"  Asiento: {fila_letra}{columna_num}")
                print(f"  Precio: ${boleto.precio:.2f}")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    def ejecutar(self):
        """Ejecutar el cliente"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.menu_peliculas()
            elif opcion == "2":
                self.menu_salas()
            elif opcion == "3":
                self.menu_funciones()
            elif opcion == "4":
                self.menu_generar_boletos()
            elif opcion == "5":
                self.listar_todos_boletos()
            elif opcion == "0":
                print("\nCerrando cliente administrador...")
                break
            else:
                print("\n✗ Opción inválida")


def main():
    """Función principal"""
    try:
        cliente = ClienteAdministrador()
        cliente.ejecutar()
    except KeyboardInterrupt:
        print("\n\nCliente cerrado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

