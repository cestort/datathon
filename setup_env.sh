#!/usr/bin/env bash
set -euo pipefail

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "No se encontró Python. Instálalo o ajusta la variable PYTHON." >&2
  exit 1
fi

echo "[1/3] Creando entorno virtual 'venv'..."
"$PYTHON" -m venv venv

echo "[2/3] Actualizando pip..."
./venv/bin/python -m pip install --upgrade pip

echo "[3/3] Instalando dependencias de requirements.txt..."
if [[ -f requirements.txt ]]; then
  ./venv/bin/pip install -r requirements.txt
else
  echo "No se encontró 'requirements.txt' en el directorio actual." >&2
  exit 1
fi

echo
echo "Listo. Activa el entorno con:"
echo "    source venv/bin/activate"
echo "Para salir del entorno: deactivate"