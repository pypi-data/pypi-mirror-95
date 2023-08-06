# dabu

## English
dabu is a python package that pulls information from the enlisted stocks on the Mexican Stock Exchange (a.k.a. BOLSA).<br><br>
Market and financial information include:
1. Market price (From Yahoo!Finance)
* End of the day price range (OHLC)
* Intraday price
    
2. Quarterly financial statements sourced from CNBV Mexico's SEC (2017Q1 forward)
* Balance Sheet
* Income Statement
* Cash Flow Statement
    

### Instalation
```
pip3 install dabu
```
### Dependecies
* [Python >=3.6](https://www.python.org) 
* [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
* [Requests](https://2.python-requests.org/en/master/)

### Usage example

#### Importing library
```python
import dabu as db
```

#### Close price for AMXL (AmericaMovil)
```python
amxl = db.Price('amxl', '2021-01-10', '2021-02-04').resultado
amxl
```
This will display `amxl` as a panda's DataFrame.

![amxl](https://drive.google.com/uc?export=view&id=1JUuT1HhsOzKnHgADwwtP1greLv53bcOK)

#### Highest Price of the day for a list of stocks
A series of stocks can be queried in bulk. Use a list instead of a string as the first argument.
Default value for `tipo_precio` is `Adjusted Close`.  Other values include `Open`, `High`, `Low` and `Close`.  

```python
high = db.Precios(['amxl', 'walmex', 'femsaubd'], '2021-01-20', '2021-02-04', tipo_precio='High').resultado
high
```
![high](https://drive.google.com/uc?export=view&id=1SFDRaQHX2f05n1VfX9eR1SOyHEPG0An_)

#### Intraday price

To get intraday prices, use the `Intraday()` method. By default the price interval is `1m`. Other values include `2m`, `5m`,
`10m`, `15m`, `30m`, `60m` and `90m`. As of this writing, Yahoo Finance keeps the last 29 days of `1m` intervals. 
```python
walmex = db.Intraday('walmex', '2021-01-30', '2021-02-04').show
walmex
```
![intraday](https://drive.google.com/uc?export=view&id=1EmqtBM-yRNLM9Mx2uC-k6x_lj01NXlBn)

### Quarterly reports
#### Initialize instance
```python
data = Financials()
``` 
#### Balance Sheet
Get the AC ("Arca Contal") Balance Sheet for 2018Q1, 2019Q1, 2020Q1 and display
the first five rows of the DaraFrame using panda's `head()` function.
```python
ac = data.balance('ac', ['2018-03-31', '2019-03-31', '2020-03-31'])
ac.head()
```
![ac_balac_s](https://drive.google.com/uc?export=view&id=1Vlh2wkJ-2a5MsTQfgdMMvdDWcgQVhVC2)

#### Income Statement
Upload WALMEX income statement for 2019Q3 and 2020Q3. The active instance, if there is one, can be used.
```python
walmex = data.income('walmex', ['2019-09-30', '2020-09-30'])
walmex.head()
```
![walmex_income](https://drive.google.com/uc?export=view&id=1Ztc19zlWXf7woDh1QjGl4aXC7DVS_UDl)

#### Cash Flow Statement
Display WALMEX Cash Flow Statement for the same interval.
```python
walmex_cf = data.flows('walmex',['2019-09-30', '2020-09-30'])
walmex_cf.head()
```
![walmex_flows](https://drive.google.com/uc?export=view&id=1CHwqK-TdOpeHPWFW5ICYPE7YWFhXsrdH)

#### Compare financial statement bewteen companies
Previously, only financial statements with the same company have been compared. Comparing values across companies can be accomplished using the `compare()` method.

```python
income = data.compare( 'income', '2020-09-30',['walmex', 'ac', 'femsa', 'cemex'])
income.head()
```

![walmex_comparar](https://drive.google.com/uc?export=view&id=1NEFp-rCtOxp22vRQ9_aS7QOdX-oTiaPE)

#### Other
A list of all stocks with financial reports can be queried using the following function.
```python
data.lista_emisoras
```

### Jupyter notebook code used in this examples
Acces the code used on this examples [JUPYTER NOTEBOOK AT GITHUB](http://bit.ly/readme_code)
If github dosn't reander the above link [JUPYTER NBVIWER](http://bit.ly/readme_code_nbviewer)

### Legal
dabu is distribuited under the BSD 3-Clause License.  See the [LICENSE.txt](http://bit.ly/dabu_license) for details.

Hope this package is usefull to you.  Please drop me a line with any sugestion, question or just to say hello!

Carlos Crespo (carlos@dabu.io)

## Español
dabu es un paquete de python enfocado en obtener infomación bursátil de las emisoras enlistadas en la Bolsa Mexicana de Valores.  En esta
versión la información es:
1. Precios de mercado (De Yahoo!Finance)
* Precio de cierre diario (AMMC)
* Precio intradía
2. Reportes trimestrales (De la CNBV, 2017Q1 al presente)
* Balance General
* Estado de Resultados
* Flujos de efectivo
    
### Instalación
```
pip3 install dabu
```
### Dependencias
* [Python 3.x](https://www.python.org) 
* [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
* [Requests](https://2.python-requests.org/en/master/)

#### Probado con las siguientes versiones
* Python 3.9.1
* Pandas 1.2.0
* Requests 2.25.1
### Ejemplo de uso

#### Importar librería
```python
import dabu as db
```

#### Precio de cierre de AMXL (AmericaMovil)
```python
amxl = db.Precios('amxl', '2021-01-10', '2021-02-04').resultado
amxl
```
Desplegara `amxl` como un DataFrame de pandas.

![amxl](https://drive.google.com/uc?export=view&id=1JUuT1HhsOzKnHgADwwtP1greLv53bcOK)

#### Precio más alto del día de una lista de emisoras
Puedes incluir una lista de tickers en lugar de una sola emisora.  Por default, `Precios` descarga el `Precio Ajustado` y
lo puedes cambiar por el precio de `apertura`, `max`, `min` o `cierre`. 

```python
maximo = db.Precios(['amxl', 'walmex', 'femsaubd'], '2021-01-20', '2021-02-04', tipo_precio='max').resultado
maximo
```
![high](https://drive.google.com/uc?export=view&id=1SFDRaQHX2f05n1VfX9eR1SOyHEPG0An_)

#### Precio Intradia
Puedes utilizar `Intradia`.  El intervalo por default es de `1m` y lo puedes cambiar a `2m`, `5m`,
`10m`, `15m`, `30m`, `60m` y `90m`.  Al parecer Yahoo! Finance solo guarda los últimos 29 días con intervalos de `1m` y no puedes
descargar un rango mayor a 7 días, utilizando intervalos de `1m`.
```python
walmex = db.Intradia('walmex', '2021-01-30', '2021-02-04').resultado
walmex
```
![intradia](https://drive.google.com/uc?export=view&id=1EmqtBM-yRNLM9Mx2uC-k6x_lj01NXlBn)

### Reportes trimestrales
#### Inicializar instancia
```python
datos = Reportes()
``` 
#### Balance General
Vamos a decargar el Balance General de AC ("Arca Contal") del 1er trimestre de 2018, 2019 y 2020.  La información
la desplegaremos utilizando el atributo `.head()` de pandas.
```python
ac = datos.balance_g('ac', ['2017-03-31','2018-03-31', '2019-03-31', '2020-03-31'])
ac.head()
```
![ac_balac_g](https://drive.google.com/uc?export=view&id=1r3V0RAb4iDQr1dOohVHt_3ToRJkR0BwR)

#### Estado de resultados
Una vez cargada la instancia, no es necesario volverla a correr para cargar nueva información.  Vamos a cargar el Estado de Resultados
de WALMEX ("WalMart de México") al tercer trimestre del 2019 y 2020.
```python
walmex = datos.restulados('walmex', ['2019-09-30', '2020-09-30'])
walmex.head()
```
![walmex_resultados](https://drive.google.com/uc?export=view&id=15UdmyCt7vyou8q3R-EvnRYFdt_jRp6dm)

#### Flujos de efectivo
Vamos a desplegar los Flujos de Efectivo de WALMEX para el mismo periodo que el Estado de Resultados.
```python
walmex_cf = datos.flujos('walmex',['2019-09-30', '2020-09-30'])
walmex_cf.head()
```
![walmex_flujos](https://drive.google.com/uc?export=view&id=1TLuF3QawOfZnV1SC73jpGd1uol2fM9R5)

#### Comparar un estado financiero entre varias emisoras
Hasta este punto, solamente hemos comparado un estado financiero contra diferentes trimestres de una misma emisora.
También podemos comprar varias emisoras en un estado financiero utilizando el método `comparar`.
```python
income = datos.comparar( 'flujos', '2020-09-30',['walmex', 'ac', 'femsa', 'cemex'])
income.head()
```

![comparar](https://drive.google.com/uc?export=view&id=1yic73CldxtfvAvE0VAbEGXv2M3wWGBE_)
#### Other
Puedes enlistar todas las emisoras que tienen erportes finacieros utilizando
```python
data.lista_emisoras
```
Recuerda que puedes utilizar todas las funcionalidades de pandas para:
* Generar señales de compra y venta en las series de tiempo
* Calcular razones financieras
* Realizar gráficas
* Grabar DataFrames a Excel o a archivo csv
* Etc.

### Legal
dabu es distribuido bajo la licencia BSD 3-Clause.  Lee el archivo [LICENSE.txt](http://bit.ly/dabu_license) para mayor información.

Espero que este paquete te sea útil.  Porfavor escribeme cualquier sugerencia, pregunta o simplemente si quieres saludar!<br>
**Carlos Crespo**
    