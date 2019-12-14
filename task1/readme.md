# Práctica 1
El objetivo de esta práctica era programar una función capaz de minimizar autómatas utilizando la clase Afd para leer autómatas de ficheros Jflap (extensión jff).

En vez de utilizar la clase Afd, hemos creado un Wrapper llamado Automaton alrededor de ella para poder utilizar el autómata como si fuese completo y no hubiese estados inaccesibles.

# Funciones
La función principal de Automaton es $\texttt{printMinimizedAutomaton()}$, que imprime el autómata ya minimizado. Esta función hace uso de las funciones internas $\texttt{triangularTable()}$ para crear una tabla triangular de acuerdo al algoritmo de minimización y $\texttt{equivStates()}$ para juntar los estados equivalentes de acuerdo a la tabla.
