from colorama import init, Fore, Style
from datetime import datetime, timedelta
import json
import os

init(autoreset=True)

ARCHIVO_DATOS = "datos_camioneta.json"


# =========================
# CARGAR Y GUARDAR DATOS
# =========================

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    else:
        return {"gastos": [], "acarreos": []}


def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(datos, f, indent=4)


datos = cargar_datos()


# =========================
# REGISTRAR GASTO
# =========================

def registrar_gasto():

    print(Fore.CYAN + "\n=== REGISTRAR GASTO ===")

    try:
        valor = int(input("Valor del gasto: "))
    except:
        print("Valor inválido")
        return

    print("Tipo de gasto:")
    print("1. Gasolina")
    print("2. Mantenimiento")
    print("3. Otros")

    tipo = input("Opción: ")

    if tipo == "1":
        tipo_str = "Gasolina"
    elif tipo == "2":
        tipo_str = "Mantenimiento"
    else:
        tipo_str = "Otros"

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos["gastos"].append({
        "valor": valor,
        "tipo": tipo_str,
        "fecha": fecha
    })

    guardar_datos(datos)

    print(Fore.GREEN + "Gasto registrado")


# =========================
# CALCULAR VALOR ACARREO
# =========================

def calcular_valor(km, tipo):

    if tipo == "1":  # sencillo

        if km <= 5:
            valor = 25000
        elif km < 50:
            valor = km * 4000
        elif km < 100:
            valor = km * 3500
        else:
            valor = km * 3000

    else:  # especial

        if km <= 5:
            valor = 25000
        elif km < 50:
            valor = km * 5000
        elif km < 100:
            valor = km * 4500
        else:
            valor = km * 4000

    return valor


# =========================
# REGISTRAR ACARREO
# =========================

def registrar_acarreo():

    print(Fore.CYAN + "\n=== REGISTRAR ACARREO ===")

    destino = input("Destino: ")

    try:
        km = float(input("Kilómetros: "))
    except:
        print("Kilómetros inválidos")
        return

    print("Tipo de acarreo")
    print("1. Sencillo")
    print("2. Especial")

    tipo = input("Opción: ")

    valor_base = calcular_valor(km, tipo)

    print("¿Hay peajes?")
    print("1. Sí")
    print("2. No")

    peajes = 0

    op = input("Opción: ")

    if op == "1":

        try:
            ida = int(input("Peaje ida: "))
            vuelta = int(input("Peaje regreso: "))
            peajes = ida + vuelta
        except:
            print("Peaje inválido")
            return

        # guardar automáticamente como gasto
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        datos["gastos"].append({
            "valor": peajes,
            "tipo": "Peajes",
            "fecha": fecha
        })

    valor_sugerido = valor_base + peajes

    print(Fore.YELLOW + f"\nValor sugerido a cobrar: {int(valor_sugerido)}")

    try:
        valor_real = int(input("Valor que realmente cobraste: "))
    except:
        print("Valor inválido")
        return

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos["acarreos"].append({
        "destino": destino,
        "km": km,
        "valor_sugerido": valor_sugerido,
        "valor_real": valor_real,
        "fecha": fecha
    })

    guardar_datos(datos)

    print(Fore.GREEN + "Acarreo registrado")


# =========================
# COTIZAR
# =========================

def cotizar():

    print(Fore.CYAN + "\n=== COTIZAR ACARREO ===")

    try:
        km = float(input("Kilómetros: "))
    except:
        print("Kilómetros inválidos")
        return

    print("Tipo de acarreo")
    print("1. Sencillo")
    print("2. Especial")

    tipo = input("Opción: ")

    valor = calcular_valor(km, tipo)

    print("¿Hay peajes?")
    print("1. Sí")
    print("2. No")

    peajes = 0

    op = input("Opción: ")

    if op == "1":
        try:
            ida = int(input("Peaje ida: "))
            vuelta = int(input("Peaje regreso: "))
            peajes = ida + vuelta
        except:
            print("Peaje inválido")
            return

    total = valor + peajes

    print(Fore.GREEN + f"\nValor estimado del acarreo: {int(total)}")


# =========================
# HISTORIAL
# =========================

def historial_acarreos():

    print(Fore.CYAN + "\n=== HISTORIAL DE ACARREOS ===")

    if not datos["acarreos"]:
        print("No hay registros")
        return

    for a in datos["acarreos"]:

        print(
            f'{a["fecha"]} | {a["destino"]} | {a["km"]} km | '
            f'Sugerido: {int(a["valor_sugerido"])} | '
            f'Cobrado: {a["valor_real"]}'
        )


# =========================
# BALANCE
# =========================

def mostrar_cuentas():

    print(Fore.CYAN + "\n=== BALANCE ===")

    print("1. Última semana")
    print("2. Último mes")
    print("3. Último año")

    opcion = input("Elige período: ")

    ahora = datetime.now()

    if opcion == "1":
        inicio = ahora - timedelta(days=7)
        periodo = "última semana"

    elif opcion == "2":
        inicio = ahora.replace(day=1)
        periodo = "último mes"

    elif opcion == "3":
        inicio = ahora.replace(month=1, day=1)
        periodo = "último año"

    else:
        print("Opción inválida")
        return

    total_acarreos = 0

    for a in datos["acarreos"]:
        fecha = datetime.strptime(a["fecha"], "%Y-%m-%d %H:%M:%S")
        if fecha >= inicio:
            total_acarreos += a["valor_real"]

    gasolina = 0
    mantenimiento = 0
    peajes = 0
    otros = 0

    for g in datos["gastos"]:

        fecha = datetime.strptime(g["fecha"], "%Y-%m-%d %H:%M:%S")

        if fecha >= inicio:

            if g["tipo"] == "Gasolina":
                gasolina += g["valor"]

            elif g["tipo"] == "Mantenimiento":
                mantenimiento += g["valor"]

            elif g["tipo"] == "Peajes":
                peajes += g["valor"]

            else:
                otros += g["valor"]

    total_gastos = gasolina + mantenimiento + peajes + otros

    print(Fore.YELLOW + f"\nBALANCE {periodo.upper()}")

    print(Fore.GREEN + f"\nAcarreos: {total_acarreos}")

    print(Fore.RED + "\nGastos:")
    print(f"Gasolina: {gasolina}")
    print(f"Mantenimiento: {mantenimiento}")
    print(f"Peajes: {peajes}")
    print(f"Otros: {otros}")

    print(Fore.YELLOW + f"\nTotal gastos: {total_gastos}")

    print(Fore.CYAN + f"\nGanancia neta: {total_acarreos - total_gastos}")


# =========================
# MENU
# =========================

def menu():

    print(Fore.CYAN + Style.BRIGHT + "\n=== MENÚ PRINCIPAL ===")

    print("1. Registrar gasto")
    print("2. Registrar acarreo")
    print("3. Cotizar acarreo")
    print("4. Historial de acarreos")
    print("5. Balance")
    print("6. Salir")


# =========================
# LOOP PRINCIPAL
# =========================

while True:

    menu()

    opcion = input(Fore.MAGENTA + "Elige una opción: ")

    if opcion == "1":
        registrar_gasto()

    elif opcion == "2":
        registrar_acarreo()

    elif opcion == "3":
        cotizar()

    elif opcion == "4":
        historial_acarreos()

    elif opcion == "5":
        mostrar_cuentas()

    elif opcion == "6":
        print("Saliendo...")
        break

    else:
        print("Opción inválida")
        
