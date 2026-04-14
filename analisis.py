import pandas as pd
import sqlite3
import numpy as np

# Leer archivo CSV
datos = pd.read_csv("jugadores.csv")

# =========================
# PROBABILIDADES JUGADORES
# =========================

# Promedio goles por partido
datos["Prom_Goles"] = datos["Goles"] / datos["Partidos"]

# Probabilidad realista de gol (Poisson)
datos["Prob_Gol"] = (
    (1 - np.exp(-datos["Prom_Goles"])) * 100
)

# Promedio asistencias
datos["Prom_Asistencias"] = (
    datos["Asistencias"] / datos["Partidos"]
)

# Probabilidad asistencia
datos["Prob_Asistencia"] = (
    (1 - np.exp(-datos["Prom_Asistencias"])) * 100
)

# Redondear a número entero
datos["Prob_Gol"] = datos["Prob_Gol"].round(0).astype(int)
datos["Prob_Asistencia"] = datos["Prob_Asistencia"].round(0).astype(int)

# =========================
# PROBABILIDADES EQUIPOS
# =========================

equipos = datos.groupby("Equipo").agg({
    "Goles": "sum",
    "Asistencias": "sum",
    "Partidos": "sum"
}).reset_index()

# Promedio ofensivo
equipos["Prom_Equipo"] = (
    (equipos["Goles"] + equipos["Asistencias"]) /
    equipos["Partidos"]
)

# Probabilidad ganar
equipos["Prob_Ganar"] = (
    (1 - np.exp(-equipos["Prom_Equipo"])) * 100
)

# Empatar
equipos["Prob_Empatar"] = (
    equipos["Prob_Ganar"] * 0.25
)

# Perder
equipos["Prob_Perder"] = (
    100 - (
        equipos["Prob_Ganar"] +
        equipos["Prob_Empatar"]
    )
)

# Redondear equipos
equipos["Prob_Ganar"] = equipos["Prob_Ganar"].round(0).astype(int)
equipos["Prob_Empatar"] = equipos["Prob_Empatar"].round(0).astype(int)
equipos["Prob_Perder"] = equipos["Prob_Perder"].round(0).astype(int)

# =========================
# GUARDAR EN BASE DE DATOS
# =========================

conexion = sqlite3.connect("betanalytics.db")

datos.to_sql(
    "jugadores",
    conexion,
    if_exists="replace",
    index=False
)

equipos.to_sql(
    "equipos",
    conexion,
    if_exists="replace",
    index=False
)

conexion.close()

conexion.close()

import matplotlib.pyplot as plt

# =========================
# GRAFICA TOP EQUIPOS
# =========================

# Ordenar por Prob_Ganar
top_equipos = equipos.sort_values(
    by="Prob_Ganar",
    ascending=False
).head(10)

plt.figure()

plt.bar(
    top_equipos["Equipo"],
    top_equipos["Prob_Ganar"]
)

plt.xticks(rotation=45)

plt.title("Top 10 Equipos con Mayor Probabilidad de Ganar")

plt.xlabel("Equipos")

plt.ylabel("Probabilidad de Ganar (%)")

plt.tight_layout()

plt.savefig("static/grafica_equipos.png")

plt.close()

print("Probabilidades actualizadas correctamente")
