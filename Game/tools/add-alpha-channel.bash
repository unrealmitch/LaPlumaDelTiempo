#!/bin/bash
# Añade canal alfa a PNGs que no lo tengan
# Functiona en Linux. Utiliza el paquete ImageMagick
#
# Ejemplo de llamada:
# /bin/bash tools/add-alpha-channel.sh images/
#
# El último parámetro es el directorio de las imágenes. 
# ¡¡ El nombre del directorio debe acabar con '/' !!

for image in $( ls $1 ); do
    convert $1$image -channel rgba -alpha set $1$image
done


