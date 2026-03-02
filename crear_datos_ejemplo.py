#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear datos de ejemplo en el sistema
"""

import sys
from datetime import datetime, timedelta
from omniORB import CORBA
import CosNaming
import Cine


def conectar_servidor():
    """Conectar al servidor CORBA"""
    try:
        orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

        try:
            # Intentar con servicio de nombres
            naming_context = orb.resolve_initial_references("NameService")
            naming_context = naming_context._narrow(CosNaming.NamingContext)
            name = [CosNaming.NameComponent("SistemaCine", "Object")]
            obj = naming_context.resolve(name)
            sistema = obj._narrow(Cine.SistemaCine)
        except:
            # Usar IOR desde archivo
            with open("servidor.ior", "r") as f:
                ior = f.read()
            obj = orb.string_to_object(ior)
            sistema = obj._narrow(Cine.SistemaCine)

        if sistema is None:
            raise Exception("No se pudo conectar al servidor")

        return sistema

    except Exception as e:
        print(f"Error al conectar: {e}")
        return None


def crear_datos_ejemplo(sistema):
    """Crear datos de ejemplo"""
    print("=" * 60)
    print("CREANDO DATOS DE EJEMPLO")
    print("=" * 60)

    try:
        # Crear películas
        print("\n1. Creando películas...")
        peliculas = [
            ("Avatar: El Camino del Agua", "Ciencia Ficción", 192),
            ("Rápidos y Furiosos 10", "Acción", 141),
            ("The Batman", "Acción", 176),
            ("Top Gun: Maverick", "Acción", 131),
            ("Jurassic World: Dominion", "Aventura", 147),
        ]

        ids_peliculas = []
        for titulo, genero, duracion in peliculas:
            try:
                id_pelicula = sistema.crearPelicula(titulo, genero, duracion)
                ids_peliculas.append(id_pelicula)
                print(f"   ✓ {titulo} (ID: {id_pelicula})")
            except Cine.ErrorValidacion as e:
                print(f"   ⚠ {titulo}: {e.mensaje}")

        # Crear salas
        print("\n2. Creando salas...")
        salas = [
            ("Sala VIP", 8, 10),
            ("Sala Premium", 10, 12),
            ("Sala Estándar 1", 12, 15),
            ("Sala Estándar 2", 12, 15),
            ("Sala IMAX", 15, 18),
        ]

        ids_salas = []
        for nombre, filas, columnas in salas:
            try:
                id_sala = sistema.crearSala(nombre, filas, columnas)
                ids_salas.append(id_sala)
                print(f"   ✓ {nombre} ({filas}x{columnas}) (ID: {id_sala})")
            except Cine.ErrorValidacion as e:
                print(f"   ⚠ {nombre}: {e.mensaje}")

        # Crear funciones
        print("\n3. Creando funciones...")

        # Obtener fecha de hoy y siguientes días de la semana
        hoy = datetime.now().date()

        # Crear funciones para los próximos días
        funciones = []
        horarios = ["10:00", "13:00", "16:00", "19:00", "22:00"]

        for dia_offset in range(5):  # Próximos 5 días
            fecha = hoy + timedelta(days=dia_offset)
            fecha_str = fecha.strftime("%Y-%m-%d")

            # Verificar si está en la semana actual
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)

            if fecha < inicio_semana or fecha > fin_semana:
                continue

            for pelicula_idx, pelicula_id in enumerate(ids_peliculas[:3]):
                for hora in horarios[:3]:  # 3 horarios por película
                    sala_id = ids_salas[pelicula_idx % len(ids_salas)]
                    funciones.append((pelicula_id, sala_id, fecha_str, hora))

        ids_funciones = []
        funciones_creadas = 0
        for pelicula_id, sala_id, fecha, hora in funciones:
            try:
                id_funcion = sistema.crearFuncion(pelicula_id, sala_id,
                                                  fecha, hora)
                ids_funciones.append(id_funcion)

                pelicula = sistema.obtenerPelicula(pelicula_id)
                sala = sistema.obtenerSala(sala_id)
                print(f"   ✓ {pelicula.titulo} - {sala.nombre} - "
                      f"{fecha} {hora} (ID: {id_funcion})")
                funciones_creadas += 1

            except Cine.ErrorValidacion as e:
                # Omitir errores de funciones duplicadas o fuera de rango
                pass

        print(f"\n   Total: {funciones_creadas} funciones creadas")

        # Generar algunos boletos de ejemplo
        print("\n4. Generando boletos de ejemplo...")
        if ids_funciones:
            nombres = ["Juan Pérez", "María García", "Carlos López",
                      "Ana Martínez", "Pedro Sánchez"]

            boletos_generados = 0
            for i, id_funcion in enumerate(ids_funciones[:5]):
                try:
                    # Generar 2-3 boletos por función
                    for j in range(2):
                        fila = j
                        columna = i * 2 + j
                        nombre = nombres[i % len(nombres)]

                        id_boleto = sistema.generarBoleto(
                            id_funcion, fila, columna, nombre, 50.0
                        )

                        if j == 0:  # Solo mostrar el primero de cada función
                            funcion = sistema.obtenerFuncion(id_funcion)
                            pelicula = sistema.obtenerPelicula(funcion.peliculaId)
                            fila_letra = chr(ord('A') + fila)
                            print(f"   ✓ {nombre} - {pelicula.titulo} - "
                                  f"Asiento {fila_letra}{columna+1} (ID: {id_boleto})")

                        boletos_generados += 1

                except Cine.ErrorValidacion:
                    pass

            print(f"\n   Total: {boletos_generados} boletos generados")

        print("\n" + "=" * 60)
        print("✓ DATOS DE EJEMPLO CREADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nResumen:")
        print(f"  - {len(ids_peliculas)} películas")
        print(f"  - {len(ids_salas)} salas")
        print(f"  - {funciones_creadas} funciones")
        print("\nYa puede usar el sistema con datos precargados.")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error al crear datos: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Función principal"""
    print("\nConectando al servidor...")
    sistema = conectar_servidor()

    if sistema is None:
        print("\n✗ No se pudo conectar al servidor.")
        print("Asegúrese de que el servidor esté ejecutándose:")
        print("  python3 servidor.py")
        sys.exit(1)

    print("✓ Conectado al servidor\n")

    respuesta = input("¿Desea crear datos de ejemplo? (s/n): ").strip().lower()

    if respuesta == 's':
        crear_datos_ejemplo(sistema)
    else:
        print("Operación cancelada.")


if __name__ == "__main__":
    main()

