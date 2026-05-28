# Recon Tool

Script de reconocimiento automatizado para pentesting y CTFs. Agrupa las herramientas más comunes (Nmap, Gobuster, FFuf, Dirb, Subfinder, WPScan, etc.) que utilizo en mi día a día en un solo menú interactivo, permitiendo elegir entre un modo **agresivo** (rápido, muchos hilos) o **silencioso** (lento, con delays para evadir detección).

## Uso

1. Ejecutar el script:

```bash
python3 main.py
```

2. Seleccionar el modo de reconocimiento:
   - **Agresivo** → Máxima velocidad, ideal para labs y CTFs.
   - **Silencioso** → Escaneo discreto, ideal para entornos reales.

3. Elegir una opción del menú principal:
   - `1` — Escaneo de puertos (Nmap)
   - `2` — Fuzzing de archivos y directorios (Gobuster, FFuf, Dirb)
   - `3` — Descubrimiento de subdominios (Subfinder, Assetfinder, FFuf, Sublist3r, Amass)
   - `4` — Fuzzing de parámetros (Curl + FFuf)
   - `5` — Escaneo de vulnerabilidades WordPress (WPScan)
   - `m` — Cambiar modo de reconocimiento
   - `x` — Salir

4. Introducir el objetivo cuando se solicite y listo.

## Requisitos

- Python 3
- Las herramientas de cada opción deben estar instaladas en el sistema (nmap, gobuster, ffuf, dirb, subfinder, wpscan, etc.)

---

> ⚠️ Este proyecto está en constante cambio y mejora. Soy un junior aprendiendo sobre ciberseguridad y pentesting, así que lo voy actualizando a medida que aprendo nuevas técnicas y herramientas.
