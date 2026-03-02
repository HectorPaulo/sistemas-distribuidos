#!/bin/bash

echo "Compilando archivo IDL..."
omniidl -bpython cine.idl

if [ $? -eq 0 ]; then
    echo "Compilación exitosa. Archivos generados en el directorio actual."
else
    echo "Error en la compilación del archivo IDL."
fi

