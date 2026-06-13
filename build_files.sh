#!/bin/bash

echo "Instalando dependências..."
pip3 install -r requirements.txt

echo "Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput