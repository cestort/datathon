@echo off
setlocal enabledelayedexpansion

REM === Detect Python ===
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PY=python"
  ) else (
    echo No se encontró Python en PATH. Instálalo o añade 'python' al PATH.
    exit /b 1
  )
)

echo [1/3] Creando entorno virtual 'venv'...
%PY% -m venv venv
if errorlevel 1 (
  echo Error creando el entorno virtual.
  exit /b 1
)

echo [2/3] Actualizando pip...
call .\venv\Scripts\python -m pip install --upgrade pip
if errorlevel 1 (
  echo Error actualizando pip.
  exit /b 1
)

echo [3/3] Instalando dependencias de requirements.txt...
if exist requirements.txt (
  call .\venv\Scripts\pip install -r requirements.txt
) else (
  echo No se encontró 'requirements.txt' en el directorio actual.
  exit /b 1
)

echo.
echo Listo. Para activar el entorno ejecuta:
echo     call venv\Scripts\activate
echo Para salir del entorno:   deactivate

endlocal