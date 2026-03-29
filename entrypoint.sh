#!/bin/bash
set -e

echo "Iniciando sistema de percepción industrial..."
# Pasamos todos los argumentos que reciba el contenedor al script main.py
python -m src.main "$@"