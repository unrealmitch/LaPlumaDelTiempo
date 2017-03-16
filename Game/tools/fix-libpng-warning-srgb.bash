#!/bin/bash
# Arregla warning del perfil SRGB
# http://stackoverflow.com/questions/22745076/libpng-warning-iccp-known-incorrect-srgb-profile
# 
# Ejecutar pasándole el directorio donde están la imágenes con '/' al final.
# Por ejemplo:
# /bin/bash fix-libpng-warning-iccp.bash imagenes/
#
mogrify $1*.png
