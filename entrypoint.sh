#!/usr/bin/env bash
set -e

echo "[entrypoint] Esperando a la base de datos..."

# leer variables de entorno (coinciden con .env)
host="${DB_HOST:-db}"
user="${DB_USER:-usuario}"
pass="${DB_PASSWORD:-clave123}"
db="${DB_NAME:-hola_db}"
port="${DB_PORT:-3306}"

# intenta conectar con mysql client (usando python/pymysql)
python - <<PY
import time, os, sys
import pymysql
host = os.getenv("DB_HOST", "$host")
user = os.getenv("DB_USER", "$user")
passwd = os.getenv("DB_PASSWORD", "$pass")
db = os.getenv("DB_NAME", "$db")
port = int(os.getenv("DB_PORT", $port))

for i in range(30):
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port)
        conn.close()
        print("[entrypoint] Base de datos lista.")
        sys.exit(0)
    except Exception as e:
        print("[entrypoint] intento", i+1, "falló:", e)
        time.sleep(2)
print("[entrypoint] No pudimos conectarnos a la BD en el tiempo esperado.")
sys.exit(1)
PY

# si llegamos aquí, ejecutamos el CMD dado en Dockerfile
exec "$@"