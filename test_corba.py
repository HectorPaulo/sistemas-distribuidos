#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que los módulos CORBA están correctamente generados
"""

import sys

def test_import():
    """Probar las importaciones"""
    print("Probando importaciones...")

    try:
        print("  - Importando omniORB...", end=" ")
        from omniORB import CORBA
        print("✓")
    except ImportError as e:
        print(f"✗ Error: {e}")
        return False

    try:
        print("  - Importando CosNaming...", end=" ")
        import CosNaming
        print("✓")
    except ImportError as e:
        print(f"✗ Error: {e}")
        print("    Nota: CosNaming es opcional si se usa IOR")

    try:
        print("  - Importando módulo Cine...", end=" ")
        import Cine
        print("✓")
    except ImportError as e:
        print(f"✗ Error: {e}")
        return False

    try:
        print("  - Importando módulo Cine__POA...", end=" ")
        import Cine__POA
        print("✓")
    except ImportError as e:
        print(f"✗ Error: {e}")
        return False

    print("\n✓ Todas las importaciones exitosas")
    return True

def test_structures():
    """Probar que las estructuras están definidas"""
    print("\nProbando estructuras CORBA...")

    try:
        import Cine

        print("  - Estructura Pelicula...", end=" ")
        pelicula = Cine.Pelicula(1, "Test", "Acción", 120)
        print("✓")

        print("  - Estructura Sala...", end=" ")
        sala = Cine.Sala(1, "Sala 1", 10, 10)
        print("✓")

        print("  - Estructura Funcion...", end=" ")
        funcion = Cine.Funcion(1, 1, 1, "2026-03-02", "18:00")
        print("✓")

        print("  - Estructura Asiento...", end=" ")
        asiento = Cine.Asiento(0, 0, False)
        print("✓")

        print("  - Estructura Boleto...", end=" ")
        boleto = Cine.Boleto(1, 1, 0, 0, "Test", 50.0)
        print("✓")

        print("  - Excepción ErrorValidacion...", end=" ")
        error = Cine.ErrorValidacion("Test")
        print("✓")

        print("\n✓ Todas las estructuras funcionan correctamente")
        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interface():
    """Probar que la interfaz está definida"""
    print("\nProbando interfaz CORBA...")

    try:
        import Cine__POA

        print("  - Interfaz SistemaCine...", end=" ")
        # Verificar que la clase existe
        assert hasattr(Cine__POA, 'SistemaCine')
        print("✓")

        print("\n✓ Interfaz definida correctamente")
        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("=" * 60)
    print("PRUEBA DE MODULOS CORBA")
    print("=" * 60)
    print()

    test1 = test_import()
    if not test1:
        print("\n✗ Fallo en las importaciones")
        sys.exit(1)

    test2 = test_structures()
    if not test2:
        print("\n✗ Fallo en las estructuras")
        sys.exit(1)

    test3 = test_interface()
    if not test3:
        print("\n✗ Fallo en la interfaz")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 60)
    print("\nEl sistema está listo para usar.")
    print("\nPara iniciar:")
    print("  1. Servidor:            python3 servidor.py")
    print("  2. Cliente Admin:       python3 cliente_admin.py")
    print("  3. Cliente Usuario:     python3 cliente_usuario.py")
    print()

if __name__ == "__main__":
    main()

