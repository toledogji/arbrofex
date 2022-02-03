# Arbrofex 📈

Identificador de oportunidades de arbitraje en el mercado de futuros

### Instalación 🔧

_Para instalar el programa simplemente se ejecuta el instalador install.sh desde una consola bash, el cual instalara los requerimientos necesarios 
para el funcionamiento del programa_

```
./install.sh
```

### Pre-requisitos 📋

_Para poder consultar las cotizaciónes es neceario completar los datos de autenticación con la cuenta de remarkets en el archivo remarket_auth.py_

```
USER = "toledogji6687"
PASSWORD = "tgjdyZ5!"
ACCOUNT = "REM6687"
```

_Ademas se debe setear en el archivo instruments.py los instrumentos con los cuales se quiere trabajar indicando el ticker del futuro como llave y el ticker
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

## Funcionamiento ⚙️

_El programa lee la lista de instrumentos configurada en el archivo instruments.py y consulta sus respectivas cotizaciones en el mercado de futuros utilizando
la libreria de pyRofex y el precio del spot utilizando yFinance, luego en base a estos datos calcula la tasa de interes implicita en el futuro y analiza, comparando la tasa de interes tomadora más baja y la tasa de interes colocadora más alta, si existe una oportunidad de arbitraje permitiendo visualizar los datos antes mencionados por consola de la siguiente manera:_

```
Ticker: YPFD/FEB22
BID:  929.1
ASK:  929.25
SPOT: 905.0999755859375
TASA IMPLICITA TOMADORA: 40.58 %  
TASA IMPLICITA COLOCADORA: 40.33 %
Mejor tasa tomadora 40.58 YPFD/FEB22 Mejor tasa colocadora 40.33 YPFD/FEB22
No hay oportunidad de arbitraje
Hr: 19:11:47
Ticker: PAMP/FEB22
BID:  175.65
ASK:  176.0
SPOT: 172.9499969482422
TASA IMPLICITA TOMADORA: 26.82 %
TASA IMPLICITA COLOCADORA: 23.74 %
Mejor tasa tomadora 26.82 PAMP/FEB22 Mejor tasa colocadora 40.33 YPFD/FEB22
Oportunidad de arbitraje tomando en PAMP/FEB22 al 26.82 y colocando en YPFD/FEB22 al 40.33
Hr: 19:16:55
```

## Test unitarios 🔩

_Para ejecutar el test unitaro sobre el modulo de operaciones de mercado se debe ejecutar el siguiente comando por consola_

```
python -m doctest -v market_operations.py

```
