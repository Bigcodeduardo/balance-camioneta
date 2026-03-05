# balance_camioneta_color_json.py

from colorama import init, Fore, Style
from datetime import datetime, timedelta
import json
import os

init(autoreset=True)

# Archivo donde se guardarán los datos
ARCHIVO_DATOS = "datos_camioneta.json"

# Función para cargar datos
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    else:
        return {"gastos": [], "acarreos": []}

# Función para guardar datos
def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(datos, f, default=str, indent=4)

datos = cargar_datos()

# Funciones principales
def registrar_gasto():
    while True:
        print(Fore.CYAN + "\n=== REGISTRAR GASTO ===")
        try:
            valor = int(input(Fore.YELLOW + "Ingresa el valor del gasto (solo números enteros): "))
        except ValueError:
            print(Fore.RED + "Por favor, ingresa un número válido.")
            continue

        print(Fore.MAGENTA + "Selecciona el tipo de gasto:")
        print("1. Gasolina")
        print("2. Mantenimiento")
        print("3. Otros")
        print("4. Salir")
        tipo = input("Opción: ")

        if tipo == "1":
            tipo_str = "Gasolina"
        elif tipo == "2":
            tipo_str = "Mantenimiento"
        elif tipo == "3":
            tipo_str = "Otros"
        elif tipo == "4":
            return
        else:
            print(Fore.RED + "Opción inválida")
            continue

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos["gastos"].append({"valor": valor, "tipo": tipo_str, "fecha": fecha})
        guardar_datos(datos)
        print(Fore.GREEN + f"Gasto registrado: {tipo_str} - {valor} a las {fecha}")
        break

def registrar_acarreo():
    while True:
        print(Fore.CYAN + "\n=== REGISTRAR ACARREO ===")
        try:
            valor = int(input(Fore.YELLOW + "Ingresa el valor del acarreo: "))
        except ValueError:
            print(Fore.RED + "Por favor, ingresa un número válido.")
            continue

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos["acarreos"].append({"valor": valor, "fecha": fecha})
        guardar_datos(datos)
        print(Fore.GREEN + f"Acarreo registrado: {valor} a las {fecha}")
        break

def cotizar():
    print(Fore.CYAN + "\n=== COTIZAR ACARREO ===")
    while True:
        try:
            km = int(input(Fore.YELLOW + "Ingresa la cantidad de kilómetros: "))
        except ValueError:
            print(Fore.RED + "Ingresa un número válido.")
            continue

        print("Tipo de acarreo:")
        print("1. Sencillo")
        print("2. Especial")
        tipo = input("Opción: ")

        if tipo == "1":
            valor_km = 4000 if km > 50 else 4000
            tipo_str = "Sencillo"
        elif tipo == "2":
            valor_km = 4500 if km > 50 else 5000
            tipo_str = "Especial"
        else:
            print(Fore.RED + "Opción inválida")
            continue

        print("¿Hay peajes?")
        print("1. Sí")
        print("2. No")
        peaje_op = input("Opción: ")

        peaje_total = 0
        if peaje_op == "1":
            try:
                peaje_total = int(input("Valor total de peajes: "))
            except ValueError:
                print(Fore.RED + "Ingresa un número válido.")
                continue
        elif peaje_op != "2":
            print(Fore.RED + "Opción inválida")
            continue

        total = km * valor_km + peaje_total
        print(Fore.GREEN + f"Valor estimado del acarreo ({tipo_str}): {total}")
        break

def mostrar_cuentas():
    print(Fore.CYAN + "\n=== BALANCE DE CUENTAS ===")
    print("1. Última semana")
    print("2. Último mes")
    print("3. Último año")
    print("4. Salir")
    opcion = input("Opción: ")

    ahora = datetime.now()

    if opcion == "1":
        periodo = ahora - timedelta(days=7)
        periodo_str = "última semana"
    elif opcion == "2":
        periodo = ahora.replace(day=1)
        periodo_str = "último mes"
    elif opcion == "3":
        periodo = ahora.replace(month=1, day=1)
        periodo_str = "último año"
    elif opcion == "4":
        return
    else:
        print(Fore.RED + "Opción inválida")
        return

    def filtrar(fecha_str):
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
        return fecha >= periodo

    total_gastos = sum(g["valor"] for g in datos["gastos"] if filtrar(g["fecha"]))
    total_gasolina = sum(g["valor"] for g in datos["gastos"] if filtrar(g["fecha"]) and g["tipo"] == "Gasolina")
    total_mantenimiento = sum(g["valor"] for g in datos["gastos"] if filtrar(g["fecha"]) and g["tipo"] == "Mantenimiento")
    total_otros = sum(g["valor"] for g in datos["gastos"] if filtrar(g["fecha"]) and g["tipo"] == "Otros")

    total_acarreo = sum(a["valor"] for a in datos["acarreos"] if filtrar(a["fecha"]))

    ganancia_neta = total_acarreo - total_gastos

    print(Fore.YELLOW + f"\nBalance de {periodo_str}:")
    print(Fore.GREEN + f"Total acarreos: {total_acarreo}")
    print(Fore.RED + f"Total gastos: {total_gastos} (Gasolina: {total_gasolina}, Mantenimiento: {total_mantenimiento}, Otros: {total_otros})")
    print(Fore.CYAN + f"Ganancia neta: {ganancia_neta}")

def mostrar_menu_principal():
    print(Fore.CYAN + Style.BRIGHT + "\n=== MENÚ PRINCIPAL ===")
    print(Fore.YELLOW + "1. Registrar gastos")
    print(Fore.YELLOW + "2. Registrar acarreo")
    print(Fore.YELLOW + "3. Cotizar")
    print(Fore.YELLOW + "4. Cuentas")
    print(Fore.RED + "5. Salir")

# Bucle principal
while True:
    mostrar_menu_principal()
    opcion = input(Fore.MAGENTA + "Elige una opción (1-5): ")

    if opcion == "1":
        registrar_gasto()
    elif opcion == "2":
        registrar_acarreo()
    elif opcion == "3":
        cotizar()
    elif opcion == "4":
        mostrar_cuentas()
    elif opcion == "5":
        print(Fore.CYAN + "Saliendo... ¡Hasta luego!")
        break
    else:
        print(Fore.RED + "Opción inválida, intenta de nuevo.")

        