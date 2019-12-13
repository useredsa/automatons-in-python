#!/usr/bin/python3
import sys
from jflap.Afd import Afd
from jflap.Transiciones import Transiciones
from tabulate import tabulate
#We have used the following modules: tabulate
 
 
class Automata:
    def __init__(self, simbolos, estados, transiciones, iniciales, finales):
        #Conjunto que contiene el alfabeto del automata
        self.simbolos = simbolos
        #Conjunto que contiene los estados del automata
        self.estados = estados
        #Diccionario que contiene las transiciones del automata 
        #-Claves: strings de la forma "id_estado"+ "estado" +"simbolo_del_alfabeto"
        #-Valor: estado del automata al aplicar la funcion de transicion
        self.transiciones = transiciones 
        #Conjunto de estados iniciales del automata
        self.iniciales = iniciales 
        #Conjunto de estados finales del automata
        self.finales = finales
    
    def getSimbolos(self):
        return self.simbolos
    def getEstados(self):
        return self.estados
    def getTransiciones(self):
        return self.transiciones
    def getInicial(self):
        return self.iniciales
    def getFinales(self):
        return self.finales
    def addTransicion(self,estado,simbolo,next_estado):
        clave = str(estado)+str(simbolo)
        self.transiciones[clave] = next_estado
        return
    def addFinales(self,estado):
        self.finales.add(estado)
        return
    def addEstado(self,estado):
        self.estados.add(estado)
        return
    def nextEstado(self,estado,simbolo):
        clave = str(estado)+str(simbolo)  
        return self.transiciones[clave]

    #Receives any automata
    #Return a complete automata without inaccessible states
def myPerfectAFD(afd):  
    simbols = afd.getAlfabeto()
    initial = afd.getEstadoInicial()
    if not initial:
        print("ERROR: This automata doesn't have initial state",file=sys.stderr)
        sys.exit(-1)
    q_error = 'q_error'
    state_list = [initial]
    myafd = Automata(simbols,set(),dict(),initial,set())
    #Breadth First Search
    while state_list:
        elem = state_list.pop(0)
        if not elem in myafd.getEstados():
            myafd.addEstado(elem)
            if afd.esFinal(elem):
                myafd.addFinales(elem)
            for i in simbols:
                next_state = afd.estadoSiguiente(elem,i)
                if next_state == None:
                    myafd.addEstado(q_error)
                    myafd.addTransicion(elem,i,q_error)
                else:
                    myafd.addTransicion(elem,i,next_state)
                    state_list.append(next_state) 
    #Add q_error transitions
    if q_error in myafd.getEstados():
        for i in myafd.getSimbolos():
            myafd.addTransicion(q_error,i,q_error)
    
    if not myafd.getFinales():
        print("WARNING: This automata doesn't have final states",file=sys.stderr)         
    return myafd   

    #Receives a final table from the Marked Triangular algorithm
    #Return an array with the equivalent states and the number of equivalent states
def equivStates(T):
    equiv = [i for i in range(len(T))]
    count = 0
    for i in range(len(T)):
        if equiv[i] == i:
            count += 1
        for j in range(i+1,len(T)):
            if not T[j][i][0]:
                equiv[j] = equiv[i]
        
    return (equiv,count)

    #Receive a table of equivalence states, the number of them and the list with the old states
    # (the indexes of the table and the list must correspond to the same state)
    # Return a pair with:
    # A dictionary that translates old states to new ones
    # A list of lists that contains equivalent states 
def buildTranslatorAndList(equiv, count, states):
    list_equiv = [[] for x in range(count)] 
    translator= {}
    back = 0
    for i in range(len(equiv)):
        if equiv[i] != i:
            list_equiv[equiv[i]].append(states[i])
            translator[states[i]] = list_equiv[equiv[i]]
            back += 1
        else: 
            list_equiv[i-back].append(states[i])  
            translator[states[i]] = list_equiv[i-back]
    return (translator, list_equiv)

    #Receive a table of the triangular table algorithm
    #and an entry of that table and mark recursively
    #that entry and the ones that are associated with it
def recursiveMark(table, entry):
    to_mark = [entry]
    while to_mark:
        o = to_mark.pop(0)
        table[o[0]][o[1]][0] = True
        #Iterate over the list of associated pairs of states
        for k in range(len(table[o[0]][o[1]][1])):
            par = table[o[0]][o[1]][1][k]
            if not table[par[0]][par[1]][0]:
                to_mark.append(tuple([par[0],par[1]]))
                table[par[0]][par[1]][0] = True                                          
    return 

    #Receives a complete automata with no inaccessible states and
    #Return a pair with:
    # A dictionary that translates old states to new ones
    # A list of lists that contains equivalent states 
def markTriangTable(myafd):
    #1. Construye una tabla T con filas desde q1 (segundo estado) hasta qn (último) y columnas desde
        #q0 (primer estado) hasta qn-1 (penúltimo);
    alphabet = myafd.getSimbolos() 
    states = list(myafd.getEstados())
    n_states = len(states)
    indices = {}
    for i in range(n_states):
        indices[states[i]] = i
    finals = myafd.getFinales()

    #2. para cada casilla(qj; qi) de T hacer:
        #3. Asocia una lista(qj; qi) de parejas de estados //inicialmente vacía
    table = [[[False,[]] for x in range(n_states)] for y in range(n_states)]

    #-----/* Marcado inicial de estados distinguibles */-----
    #4. para cada casilla(qj; qi) de T hacer:
        #5. si en la pareja (qj; qi) uno es final y el otro no entonces marcar(casilla(qj; qi));                
    for i in range(n_states):
        for j in range(i):
            if (states[i] in finals) ^ (states[j] in finals):
                table[i][j][0] = True
        
    #-----/* Deducción de estados distinguibles */------
    #6. para cada casilla(qj; qi) de T hacer: //ej., realizar recorrido por filas de la tabla
    for j in range(1, n_states, 1):
        for i in range(j): 
            if not table[j][i][0]:
                for s in alphabet:
                    #7. e1 := delta(qj; a_k); e2 := delta(qi; a_k); // obtiene pareja de estados leyendo a_k
                    state1 = myafd.nextEstado(states[i],s)
                    state2 = myafd.nextEstado(states[j],s) 
                    e1, e2 = indices[state1], indices[state2]
                    if e1 <= e2:
                        e1,e2 = e2,e1
                    if table[e1][e2][0]:
                        #8. marcarRecursivamente (casilla(qj; qi));
                        recursiveMark(table, tuple([j,i]))
                        #9. break; //no prueba con más símbolos, porque (qj; qi) son distinguibles
                        #// pasa a tratar la siguiente casilla
                        break
                    #10. si-no si (e1 != e2) y casilla(e1; e2) != casilla(qj; qi) entonces
                    elif e1!=e2 and (e1!=j or e2!=i):
                        #11. añade la pareja actual (qj; qi) a la lista de pareja obtenida: lista(e1; e2);
                        table[e1][e2][1].append(tuple([j,i]))
    #12. //fin de marcado de tabla triangular
    
    equiv_and_count = equivStates(table)
    return buildTranslatorAndList(equiv_and_count[0], equiv_and_count[1], states)

    #Receive a complete automata without inaccessible states
    # and write to the console the representation of the minimize automata
def minimizeAFD(myafd):
    translator_and_min_states = markTriangTable(myafd) 
    translator = translator_and_min_states[0]
    min_states = translator_and_min_states[1]
    simbols = list(myafd.getSimbolos())
    
    #Show the formatted answer
    table = [[] for x in min_states] 
    for x in range(len(min_states)):
        element = ""
        if myafd.getInicial() in min_states[x]:
            element += "->"
        for elem in myafd.getFinales():
            if elem in min_states[x]:
                element += "#"
                break 
        element += repr(min_states[x])    
        table[x].append(element)
        
    for y in range(len(simbols)):
        for x in range(len(min_states)):
            table[x].append(repr(translator[myafd.nextEstado(min_states[x][0], simbols[y])]))   
    headers = ["States"]
    headers[1:] = simbols[0:]
        
    print(tabulate(table,headers, tablefmt="psql"))
    return
       
if __name__ == '__main__':
    #Request a JFLAP file
    name = False
    ruta = input('Enter an input file:') 
    while not name:
        if not ruta:
            sys.exit(0)    
        try:   
            automata = Afd(ruta)
            name = True
        except FileNotFoundError:
            print('The file doesn\'t exist',file=sys.stderr)
            ruta = input('Enter an input file:')
        except Exception as error:
            print('Problems: ',error,file=sys.stderr)
            sys.exit(0)
    
    #Create a complete automata without inaccessible states 
    myafd = myPerfectAFD(automata)
    #Minimize the Automaton:
    minimizeAFD(myafd)

    
    
    
    

