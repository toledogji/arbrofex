# Arbrofex

Identificador de oportunidades de arbitraje en el mercado de futuros

### Instalación 🔧

_Para instalar el programa simplemente se ejecuta el instalador install.sh desde una consola bash, el cual instalara los requerimientos necesarios 
para el funcionamiento del programa_

```
./install.sh
```

### Pre-requisitos 📋

_Se debe setear en el archivo instruments.py los instrumentos con los cuales se quiere trabajar indicando el ticker del futuro como llave y el ticker
del instrumento en spot correspondiente a Yahoo Finance como valor (Ej: "GGAL/FEB22": "GGAL")_

```
instruments = {
    "GGAL/FEB22": "GGAL",
    "PAMP/FEB22": "PAMP.BA",
    "YPFD/FEB22": "YPFD.BA",
    "DLR/FEB22": "ARS=X"
}
```

## Ejecucion ⚙️

_Para correr el programa se debe ejecutar el siguiente comando por consola_


```
py arbarofex.py
```

## Test unitarios ⚙️

_Para ejecutar el test unitaro sobre el modulo de operaciones de mercado se debe ejecutar el siguiente comando por consola_

```
python -m doctest -v market_operations.py

```
