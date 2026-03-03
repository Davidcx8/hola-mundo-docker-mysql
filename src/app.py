import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "cambiame_ahora")  # para flash messages

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "usuario")
DB_PASSWORD = os.getenv("DB_PASSWORD", "clave123")
DB_NAME = os.getenv("DB_NAME", "hola_db")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# función que intenta conectar varias veces (útil si el contenedor arranca antes que MySQL)
def get_connection(retries=12, delay=3):
    last_exc = None
    for attempt in range(retries):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            return conn
        except Exception as e:
            last_exc = e
            print(f"[DB] intento {attempt+1}/{retries} falló: {e}")
            time.sleep(delay)
    raise last_exc

@app.route("/", methods=["GET"])
def index():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, mensaje, fecha FROM visitas ORDER BY id DESC LIMIT 100;")
            rows = cur.fetchall()
        conn.close()
        return render_template("index.html", nombres=rows)
    except Exception as e:
        # si la BD no está, mostramos la página con mensaje de error (no crash)
        flash("La base de datos no está disponible ahora. Intenta en unos segundos.", "danger")
        return render_template("index.html", nombres=[])

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form.get("nombre", "").strip()
    # validación sencilla
    if not nombre:
        flash("El nombre no puede estar vacío.", "warning")
        return redirect(url_for("index"))
    if len(nombre) > 100:
        flash("Nombre demasiado largo.", "warning")
        return redirect(url_for("index"))

    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # consulta parametrizada para evitar inyecciones
            cur.execute("INSERT INTO visitas (mensaje) VALUES (%s);", (nombre,))
            conn.commit()
        conn.close()
        flash("Nombre agregado correctamente ✅", "success")
    except Exception as e:
        flash("No se pudo guardar en la base de datos: " + str(e), "danger")
    # Post-Redirect-Get para evitar reenvío de formulario
    return redirect(url_for("index"))

if __name__ == "__main__":
    # en local, para debug
    app.run(host="0.0.0.0", port=5000)