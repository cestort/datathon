Param(
  [string]$Python = "py"
)

Write-Host "[1/3] Creando entorno virtual 'venv'..."
try {
  & $Python -m venv venv
} catch {
  Write-Error "No se pudo crear el entorno virtual. Asegúrate de tener Python instalado y accesible."
  exit 1
}

Write-Host "[2/3] Actualizando pip..."
& .\venv\Scripts\python -m pip install --upgrade pip

if (-Not (Test-Path -Path ".\requirements.txt")) {
  Write-Error "No se encontró 'requirements.txt' en el directorio actual."
  exit 1
}

Write-Host "[3/3] Instalando dependencias de requirements.txt..."
& .\venv\Scripts\pip install -r requirements.txt

Write-Host "`nListo. Activa el entorno con: `n    .\venv\Scripts\Activate.ps1"
Write-Host "Para salir del entorno: deactivate"