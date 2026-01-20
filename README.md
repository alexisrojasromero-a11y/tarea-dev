Tarea – Cálculo de paneles

En esta tarea implementé una solución para calcular cuántos paneles rectangulares caben dentro de un techo, dependiendo de la forma del techo. El objetivo es devolver un número entero con la cantidad de paneles que se pueden acomodar sin superponerse y permitiendo rotarlos.

El código principal está en:

junior/python/main.py

Al correr el archivo aparece un menú:

Opción 1: corre los tests del template (usa test_cases.json).

Opción 2: modo interactivo para ingresar medidas manualmente.

Ejercicio principal (techo rectangular)
Qué se pide

El ejercicio principal pide una sola función:

calculate_panels(panel_width, panel_height, roof_width, roof_height) -> int

Esta función recibe el tamaño del panel y el tamaño del techo (ambos rectángulos) y debe devolver el máximo de paneles que caben. Se permite poner los paneles en cualquier orientación (o sea, también rotarlos).

Lógica que utilicé

Mi solución parte desde lo más simple y luego agrega una mejora práctica:

Caso base (grilla normal)

Calculo cuántos paneles caben si los pongo todos “derechos”, como una grilla:

(roof_width // panel_width) * (roof_height // panel_height)

Luego hago lo mismo pero con el panel rotado:

(roof_width // panel_height) * (roof_height // panel_width)

Me quedo con el mayor de los dos.

Mejora
En algunos casos se pueden meter más paneles si no se usa una sola orientación en todo el techo.
Para esto, probé dividir el techo en dos partes y mezclar:

una parte con paneles normales

la otra con paneles rotados

Hice esto de dos formas:

cortes verticales (izquierda y derecha)

cortes horizontales (arriba y abajo)

Para cada corte calculo:

paneles en la parte 1 + paneles en la parte 2
y me quedo con el máximo resultado encontrado.

Por qué elegí este enfoque

No busqué un “óptimo matemático” súper complejo porque el problema general de acomodar rectángulos puede crecer mucho en combinaciones.
En cambio, elegí una solución que:

es rápida,

fácil de explicar,

y mejora el resultado del caso base sin complicar demasiado el código.

Bonus 1

Para el triángulo, el techo no tiene el mismo ancho en todas partes: se va angostando hacia arriba.

Lo resolví así:

Divido el triángulo en filas del alto del panel.

En cada fila calculo el ancho disponible del triángulo.

Calculo cuántos paneles caben en esa fila y los sumo.

Para evitar contar paneles que “parecen caber” pero arriba ya no caben, tomo el ancho en el punto más angosto de la fila (la parte superior de esa franja).
También pruebo panel normal y panel rotado y me quedo con el mejor.

Bonus 2 

Este bonus modela un techo que se forma con dos rectángulos del mismo tamaño superpuestos (desplazados por dx y dy).

Mi enfoque fue:

Represento los dos rectángulos.

Para no contar dos veces la parte donde se traslapan, separo la figura en partes rectangulares sin superposición (partes “disjuntas”).

En cada parte aplico la misma lógica del ejercicio principal (calculate_panels) y luego sumo los resultados.

Este enfoque me permite reutilizar la solución base y mantener el código ordenado.

