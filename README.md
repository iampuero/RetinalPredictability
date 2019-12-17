# RetinalPredictability
:page_facing_up: Código de memoria :star:

### Datos Analizados

Los datos utilizados contienen las matrices de tiempos de disparo de 4 retinas bajo 6 condiciones distintas.

| Índice | Código | Detalle           |
| :----: | :----: | ----------------- |
|   0    |  issa  | Oscuridad Inicial |
|   1    |  ifsa  | Luz Inicial       |
|   2    |   wn   | White Noise       |
|   3    |   nm   | Natural Movie     |
|   4    |  ffsa  | Luz Final         |
|   5    |  fssa  | Oscuridad Final   |

Esta matriz de tiempos de disparo es binarizada en base a un tiempo de intervalo entre los 1[ms] a 10[ms].

Para obtener una matriz con los estados binarizados de disparo de cada neurona en el tiempo.

## Estructura de Carpetas

* Code - Códigos en python
  * External - Librerías externas (JITD)
  * MatlabIsing - Implementación de Ferrari MaxEnt (Matlab)
      * {-|mi|r}{Models|Rasters}
      * _ - Selección aleatoria por cada número de neuronas
      * mi - Selección en base a ranking de MI
      * r - Selección en base a coeficiente R^2
  * PyIsing - Impementación de Herzog de MaxEnt (Python)
* Data - Datos guardados
  * Graphs - Grafos generados
  * PreComputed - Medidas pre-computadas para cargar
    * AIS - Active Information Storage
    * H - Entropy
    * MI - Mutual Information
    * TE - Transfer Entropy
  * Sparse - Guardado de matrices Numpy-Sparse
* Documents - Documentación del trabajo

#### Formato de Archivos

Los archivos creados tienen la siguiente estructura:

``E<experimento>_C<condicion>_T<binT>.npy``

Donde la ubicación del archivo determina su contenido.


## Notas
* Se debe colocar el archivo de rasters en la carpeta Data [spktimes_4_exps_6_conds.mat](https://drive.google.com/open?id=0BxLVeqeP4TRkN3VIRlFvZlJkYVE) para la generación en caliente de los datos pre-computados

#### Software Recomendado
* [Python 3.5+](https://www.python.org/) para la ejecución del código
* [Jupyter](https://jupyter.org/) para la visualización de los ipython notebook
* [Typora](https://typora.io/) para la visualización de los archivos .md 
* [Gephi](https://gephi.org/) para la visualización de los grafos
* [JITD](https://github.com/jlizier/jidt), incluído en el repositorio (cálculo de métricas de TI)





