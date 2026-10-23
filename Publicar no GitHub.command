#!/usr/bin/env bash
cd "$(dirname "$0")"
./publicar.sh
echo
read -n 1 -s -r -p "Pronto. Pressione qualquer tecla para fechar."
