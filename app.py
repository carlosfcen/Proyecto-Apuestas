from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ======================
# PAGINA PRINCIPAL
# ======================

@app.route("/", methods=["GET", "POST"])
def inicio():

    conexion = sqlite3.connect("betanalytics.db")
    cursor = conexion.cursor()

    buscar = ""

    if request.method == "POST":
        buscar = request.form["buscar"]

        cursor.execute("""
SELECT * FROM jugadores
WHERE Jugador LIKE ?
ORDER BY Prob_Gol DESC
""", ('%' + buscar + '%',))

    else:

        cursor.execute("""
SELECT * FROM jugadores
ORDER BY Prob_Gol DESC
""")

    jugadores = cursor.fetchall()

    conexion.close()

    return render_template(
        "index.html",
        jugadores=jugadores,
        buscar=buscar
    )

# ======================
# PAGINA EQUIPOS
# ======================

@app.route("/equipos")
def equipos():

    conexion = sqlite3.connect("betanalytics.db")
    cursor = conexion.cursor()

    cursor.execute("""
SELECT * FROM equipos
ORDER BY Prob_Ganar DESC
""")

    equipos = cursor.fetchall()

    conexion.close()

    return render_template(
        "equipos.html",
        equipos=equipos
    )

if __name__ == "__main__":
    app.run(debug=True)