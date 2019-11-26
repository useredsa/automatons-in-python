#!/usr/bin/python3
import sys
from jflap.Afd import *
from jflap.Transiciones import *
from time import sleep
import tabulate

def completeAFD(M):
    
    
    return

def deleteInaccesibles(M):
    
    
    return

def markTriangTable(M):
    
    
    return

def minimizeAFD(M):
    
    
    return
       
if __name__ == '__main__':
    #Request a JFLAP file
    name = True
    ruta = input('Enter an input file:')
    while name:
        if not ruta:
            sys.exit(0)    
        try:   
            automata = Afd(ruta)
            name = False
        except FileNotFoundError:
            print('El fichero no existe ',file=sys.stderr)
            ruta = input('Enter an input file:')
        except Exception as error:
            print('Problemas: ',error,file=sys.stderr)
            sys.exit(0)
    
    #Minimize the Automaton:
    #(1) Remove accessible states and generates a complete automaton
    
    #(2) Get the set of states of the minimum automaton
    
    #(3) Get the initial state of the minimum automaton
    
    #(4) Get the set of final states of the minimum automaton
    
    #(5) Get the transitions of the minimum automaton
    
    
    #(6) Show the formatted answer
        #https://pypi.org/project/tabulate/
    #print(tabulate(table, headers, tablefmt="psql"))
    
    
    
    

