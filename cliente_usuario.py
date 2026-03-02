#!/usr/bin/env python3
import sys

import Cine
import CosNaming
from omniORB import CORBA


class ClienteUsuario:
    """Cliente para funciones de usuario del cine"""

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
            print("CLIENTE USUARIO - SISTEMA DE CINE")
            print("=" * 60)
            print("Conectado al servidor correctamente\n")

        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            sys.exit(1)

    def mostrar_menu_principal(self):
        """Mostrar menú principal"""
        print("\n" + "=" * 60)
        print("MENU USUARIO")
        print("=" * 60)
        print("1. Ver cartelera (todas las películas)")
        print("2. Ver funciones disponibles")
        print("3. Comprar boletos")
        print("0. Salir")
        print("=" * 60)

    def ver_cartelera(self):
        """Ver todas las películas disponibles"""
        print("\n" + "-" * 60)
        print("CARTELERA")
        print("-" * 60)

        try:
            peliculas = self.sistema.obtenerPeliculas()

            if not peliculas:
                print("No hay películas en cartelera")
                return

            for p in peliculas:
                print(f"\n{p.titulo}")
                print(f"  Género: {p.genero}")
                print(f"  Duración: {p.duracion} minutos")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    def ver_funciones(self):
        """Ver funciones disponibles"""
        print("\n" + "-" * 60)
        print("FUNCIONES DISPONIBLES")
        print("-" * 60)

        try:
            print("\n1. Ver todas las funciones")
            print("2. Ver funciones por fecha")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.listar_todas_funciones()
            elif opcion == "2":
                self.listar_funciones_por_fecha()
            else:
                print("Opción inválida")

        except Exception as e:
            print(f"\n✗ Error: {e}")

    def listar_todas_funciones(self):
        """Listar todas las funciones"""
        try:
            funciones = self.sistema.obtenerFunciones()

            if not funciones:
                print("No hay funciones disponibles")
                return

            # Agrupar por fecha
            funciones_por_fecha = {}
            for f in funciones:
                if f.fecha not in funciones_por_fecha:
                    funciones_por_fecha[f.fecha] = []
                funciones_por_fecha[f.fecha].append(f)

            # Mostrar agrupadas
            for fecha in sorted(funciones_por_fecha.keys()):
                print(f"\n{fecha}")
                print("-" * 40)

                for f in sorted(funciones_por_fecha[fecha],
                              key=lambda x: x.hora):
                    pelicula = self.sistema.obtenerPelicula(f.peliculaId)
                    sala = self.sistema.obtenerSala(f.salaId)

                    # Contar asientos disponibles
                    asientos = self.sistema.obtenerAsientosFuncion(f.id)
                    disponibles = sum(1 for a in asientos if not a.ocupado)

                    print(f"  [{f.id}] {f.hora} - {pelicula.titulo}")
                    print(f"      Sala: {sala.nombre} | "
                          f"Disponibles: {disponibles}/{len(asientos)}")

        except Exception as e:
            print(f"Error: {e}")

    def listar_funciones_por_fecha(self):
        """Listar funciones de una fecha específica"""
        try:
            fecha = input("\nFecha (YYYY-MM-DD): ").strip()
            funciones = self.sistema.obtenerFuncionesPorFecha(fecha)

            if not funciones:
                print(f"No hay funciones para la fecha {fecha}")
                return

            print(f"\nFunciones del {fecha}")
            print("-" * 40)

            for f in sorted(funciones, key=lambda x: x.hora):
                pelicula = self.sistema.obtenerPelicula(f.peliculaId)
                sala = self.sistema.obtenerSala(f.salaId)

                # Contar asientos disponibles
                asientos = self.sistema.obtenerAsientosFuncion(f.id)
                disponibles = sum(1 for a in asientos if not a.ocupado)

                print(f"\n  [{f.id}] {f.hora} - {pelicula.titulo}")
                print(f"      Sala: {sala.nombre}")
                print(f"      Disponibles: {disponibles}/{len(asientos)} asientos")

        except Exception as e:
            print(f"Error: {e}")

    def comprar_boletos(self):
        """Comprar boletos para una función"""
        print("\n" + "-" * 60)
        print("COMPRAR BOLETOS")
        print("-" * 60)

        try:
            # Mostrar funciones disponibles
            funciones = self.sistema.obtenerFunciones()
            if not funciones:
                print("No hay funciones disponibles")
                return

            print("\nFunciones disponibles:")
            for f in funciones:
                pelicula = self.sistema.obtenerPelicula(f.peliculaId)
                sala = self.sistema.obtenerSala(f.salaId)

                asientos = self.sistema.obtenerAsientosFuncion(f.id)
                disponibles = sum(1 for a in asientos if not a.ocupado)

                print(f"\n  [{f.id}] {pelicula.titulo}")
                print(f"      Fecha: {f.fecha} | Hora: {f.hora}")
                print(f"      Sala: {sala.nombre}")
                print(f"      Disponibles: {disponibles}/{len(asientos)}")

            funcion_id = int(input("\nID de la función: ").strip())

            # Mostrar mapa de asientos
            self.mostrar_mapa_asientos(funcion_id)

            # Solicitar información
            nombre = input("\nSu nombre: ").strip()
            precio = 50.0  # Precio fijo

            print(f"\nPrecio por boleto: ${precio:.2f}")
            print("\nSeleccione asientos (ej: A5, B10)")
            print("Escriba 'fin' cuando termine")

            asientos = []
            funcion = self.sistema.obtenerFuncion(funcion_id)
            sala = self.sistema.obtenerSala(funcion.salaId)

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

            # Mostrar resumen
            total = precio * len(asientos)
            print("\n" + "=" * 60)
            print("RESUMEN DE COMPRA")
            print("=" * 60)
            print(f"Función: {funcion_id}")
            print(f"Cantidad de boletos: {len(asientos)}")
            print(f"Precio unitario: ${precio:.2f}")
            print(f"Total: ${total:.2f}")
            print("-" * 60)

            confirmar = input("¿Confirmar compra? (s/n): ").strip().lower()

            if confirmar != 's':
                print("Compra cancelada")
                return

            # Generar boletos
            if len(asientos) == 1:
                id_boleto = self.sistema.generarBoleto(
                    funcion_id, asientos[0][0], asientos[0][1],
                    nombre, precio
                )
                self.mostrar_boleto(id_boleto)
            else:
                filas = [a[0] for a in asientos]
                columnas = [a[1] for a in asientos]
                boletos = self.sistema.generarBoletosMultiples(
                    funcion_id, filas, columnas, nombre, precio
                )
                self.mostrar_boletos_multiples(boletos)

            print("\n✓ Compra realizada exitosamente")

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
            pelicula = self.sistema.obtenerPelicula(funcion.peliculaId)
            asientos = self.sistema.obtenerAsientosFuncion(funcion_id)

            print("\n" + "=" * 60)
            print("MAPA DE ASIENTOS")
            print("=" * 60)
            print(f"Película: {pelicula.titulo}")
            print(f"Sala: {sala.nombre}")
            print(f"Fecha: {funcion.fecha} | Hora: {funcion.hora}")
            print("-" * 60)
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

            print("\n" + "-" * 60)
            print("PANTALLA")
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
            print("BOLETO")
            print("=" * 60)
            print(f"Boleto #: {boleto.id}")
            print(f"Cliente: {boleto.nombreCliente}")
            print("-" * 60)
            print(f"Película: {pelicula.titulo}")
            print(f"Género: {pelicula.genero}")
            print(f"Duración: {pelicula.duracion} minutos")
            print("-" * 60)
            print(f"Sala: {sala.nombre}")
            print(f"Fecha: {funcion.fecha}")
            print(f"Hora: {funcion.hora}")
            print(f"Asiento: {fila_letra}{columna_num}")
            print("-" * 60)
            print(f"Precio: ${boleto.precio:.2f}")
            print("=" * 60)
            print("Gracias por su compra!")
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
            print("BOLETOS")
            print("=" * 60)
            print(f"Cliente: {primer_boleto.nombreCliente}")
            print("-" * 60)
            print(f"Película: {pelicula.titulo}")
            print(f"Género: {pelicula.genero}")
            print(f"Duración: {pelicula.duracion} minutos")
            print("-" * 60)
            print(f"Sala: {sala.nombre}")
            print(f"Fecha: {funcion.fecha}")
            print(f"Hora: {funcion.hora}")
            print("-" * 60)
            print("Asientos:")

            for boleto in boletos:
                fila_letra = chr(ord('A') + boleto.fila)
                columna_num = boleto.columna + 1
                print(f"  Boleto #{boleto.id} - {fila_letra}{columna_num} "
                      f"- ${boleto.precio:.2f}")

            print("-" * 60)
            print(f"Cantidad de boletos: {len(boletos)}")
            print(f"Total: ${total:.2f}")
            print("=" * 60)
            print("Gracias por su compra!")
            print("=" * 60)

        except Exception as e:
            print(f"Error al mostrar boletos: {e}")

    def ejecutar(self):
        """Ejecutar el cliente"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.ver_cartelera()
            elif opcion == "2":
                self.ver_funciones()
            elif opcion == "3":
                self.comprar_boletos()
            elif opcion == "0":
                print("\nGracias por usar nuestro sistema. ¡Hasta pronto!")
                break
            else:
                print("\n✗ Opción inválida")


def main():
    """Función principal"""
    try:
        cliente = ClienteUsuario()
        cliente.ejecutar()
    except KeyboardInterrupt:
        print("\n\nCliente cerrado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

