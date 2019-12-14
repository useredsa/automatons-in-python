# Práctica 3
El objetivo de esta práctica es utilizar expresiones regulares para poder insertar guiones en palabras para escribir textos con un número máximo de caracteres por línea.

Como tarea adicional, hemos integrado el programa con la librería speech de google.

# Estructura de ficheros
El fichero $\texttt{TextFormatter.py}$ define la clase $\texttt{SpanishFormatter}$ que sirve para dividir textos utilizando las reglas gramaticales del español. Aquí es donde se encuentra toda la lógica del programa y la utilización de expresiones regulares. Esta clase da soporte a programas que quieran formatear textos.

Los ficheros $\texttt{FileFormat.py}$ y $\texttt{VoiceRecognition.py}$ utilizan el módulo anterior para formatear ficheros de texto y texto reconocido por voz, respectivamente. Ambos son pequeños scripts, pues toda la lógica se encuentra en el fichero $\texttt{TextFormatter.py}$.