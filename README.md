# Didácticos IIQ2013

Repositorio mínimo del curso con recurso interactivo en Marimo:

- `recursos/00_moody.py`

## Requisitos de instalación

## 1) Python 3.12 (Windows)

Instalar con winget:

```powershell
winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
```

## 2) Paquetes Python necesarios

```powershell
python -m pip install --upgrade pip
python -m pip install marimo numpy matplotlib ipywidgets
```

Si `python` no está en PATH, usar ruta completa:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m pip install --upgrade pip
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m pip install marimo numpy matplotlib ipywidgets
```

## 3) (Opcional) VS Code + extensiones

Instalar VS Code:

```powershell
winget install -e --id Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements
```

Extensiones recomendadas:

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

## Ejecutar el recurso de Moody

Desde la raíz del repo:

```powershell
marimo run recursos/00_moody.py
```

Si `marimo` no está en PATH:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\Scripts\marimo.exe" run "recursos/00_moody.py"
```

URL local esperada:
- `http://127.0.0.1:2718`

## Ejecutar en MoLab

Versión `main`:

- https://molab.marimo.io/github/nfgajardo/didactos-de-IIQ2013/blob/main/recursos/00_moody.py

Versión fija por commit (evita caché):

- https://molab.marimo.io/github/nfgajardo/didactos-de-IIQ2013/blob/441a51d/recursos/00_moody.py
