
from colorama import init, Fore, Style
init(autoreset=True)
import json
from datetime import datetime
import matplotlib.pyplot as plt
import os

# Archivo para guardar datos
DATA_FILE = "datos.json"

# Cargar datos si existen
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        datos = json.load(f)
else:
    datos = {"acarreos": [], "gastos": []}

# Función para guardar datos
def guardar_datos():
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f, indent=4)

# Función para registrar gasto
def registrar_gasto():
    while True:
        try:
            monto = int(input("Ingrese el monto del gasto en números enteros: "))
            break
        except ValueError:
            print("Debe ingresar un número entero.")
    print("Tipos de gasto:")
    print("1. Gasolina")
    print("2. Mantenimiento")
    print("3. Otros")
    tipo = input("Elija el tipo de gasto (1-3): ")
    tipos = {"1": "Gasolina", "2": "Mantenimiento", "3": "Otros"}
    tipo = tipos.get(tipo, "Otros")
    fecha = datetime.now().isoformat()
    datos["gastos"].append({"monto": monto, "tipo": tipo, "fecha": fecha})
    guardar_datos()
    print("Gasto registrado con éxito.\n")

# Función para registrar acarreo
def registrar_acarreo():
    while True:
        try:
            valor = int(input("Ingrese el valor del acarreo en números enteros: "))
            break
        except ValueError:
            print("Debe ingresar un número entero.")
    fecha = datetime.now().isoformat()
    datos["acarreos"].append({"valor": valor, "fecha": fecha})
    guardar_datos()
    print("Acarreo registrado con éxito.\n")

# Función para cotizar acarreo
def cotizar():
    while True:
        try:
            km = float(input("Ingrese la cantidad de kilómetros: "))
            break
        except ValueError:
            print("Debe ingresar un número válido.")
    print("Tipo de acarreo:")
    print("1. Especial")
    print("2. Sencillo")
    tipo = input("Elija 1 o 2: ")
    tipo_tarifa = "Especial" if tipo == "1" else "Sencillo"

    print("¿Hay peajes?")
    print("1. Sí")
    print("2. No")
    hay_peaje = input("Opción: ")
    total_peaje = 0
    if hay_peaje == "1":
        while True:
            try:
                total_peaje = int(input("Ingrese el valor total de los peajes: "))
                break
            except ValueError:
                print("Debe ingresar un número entero.")
    
    # Cálculo del acarreo según reglas de tarifas
    if km <= 5:
        tarifa = 25000
    elif km < 50:
        tarifa = 5000 if tipo_tarifa == "Especial" else 4000
        tarifa *= km
    elif km < 100:
        tarifa = 4500 if tipo_tarifa == "Especial" else 3500
        tarifa *= km
    else:
        tarifa = 4000 if tipo_tarifa == "Especial" else 3000
        tarifa *= km
    total = tarifa + total_peaje
    print(f"\nValor total del acarreo ({tipo_tarifa}): ${total}\n")

# Función para mostrar balances
def mostrar_cuentas():
    if not datos["acarreos"] and not datos["gastos"]:
        print("No hay registros para mostrar.\n")
        return
    print("Mostrar balances por:")
    print("1. Semana")
    print("2. Mes")
    print("3. Año")
    opcion = input("Elija una opción (1-3): ")
    balances = {}
    for g in datos["gastos"]:
        fecha = datetime.fromisoformat(g["fecha"])
        if opcion == "1":
            key = fecha.isocalendar()[1]  # Semana del año
        elif opcion == "2":
            key = fecha.month
        else:
            key = fecha.year
        balances.setdefault(key, {"Gasolina":0,"Mantenimiento":0,"Otros":0,"Ingresos":0})
        balances[key][g["tipo"]] += g["monto"]
    for a in datos["acarreos"]:
        fecha = datetime.fromisoformat(a["fecha"])
        if opcion == "1":
            key = fecha.isocalendar()[1]
        elif opcion == "2":
            key = fecha.month
        else:
            key = fecha.year
        balances.setdefault(key, {"Gasolina":0,"Mantenimiento":0,"Otros":0,"Ingresos":0})
        balances[key]["Ingresos"] += a["valor"]

    # Mostrar tabla de balances
    print("\nBalance acumulativo:")
    for k, v in sorted(balances.items()):
        total_gastos = v["Gasolina"] + v["Mantenimiento"] + v["Otros"]
        ganancia_neta = v["Ingresos"] - total_gastos
        print(f"Periodo {k}: Ingresos: {v['Ingresos']}, Gastos: {total_gastos} (Gasolina: {v['Gasolina']}, Mantenimiento: {v['Mantenimiento']}, Otros: {v['Otros']}), Ganancia neta: {ganancia_neta}")

    # Graficar ingresos vs gastos
    keys = list(sorted(balances.keys()))
    ingresos = [balances[k]["Ingresos"] for k in keys]
    gastos_totales = [balances[k]["Gasolina"]+balances[k]["Mantenimiento"]+balances[k]["Otros"] for k in keys]

    plt.figure(figsize=(10,5))
    plt.bar(keys, ingresos, label="Ingresos", alpha=0.7)
    plt.bar(keys, gastos_totales, bottom=ingresos, label="Gastos totales", alpha=0.7)
    plt.xlabel("Periodo")
    plt.ylabel("Monto")
    plt.title("Ingresos y Gastos")
    plt.legend()
    plt.show()

# Menú principal
def menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar gasto")
        print("2. Registrar acarreo")
        print("3. Cotizar acarreo")
        print("4. Mostrar cuentas")
        print("5. Salir")
        opcion = input("Elija una opción (1-5): ")
        if opcion == "1":
            registrar_gasto()
        elif opcion == "2":
            registrar_acarreo()
        elif opcion == "3":
            cotizar()
        elif opcion == "4":
            mostrar_cuentas()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecutar menú
if __name__ == "__main__":
    menu_principal()