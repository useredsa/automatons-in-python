#!/usr/bin/python3
import sys
from jflap.Afd import Afd
from jflap.Transiciones import Transiciones
from tabulate import tabulate
#We have used the following modules: tabulate
 
    #Class Automata... 
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
    #TODO Control de errores por si afd no es de clase Afd
def myPerfectAFD(afd):  
    simbolos = afd.getAlfabeto()
    inicial = afd.getEstadoInicial()
    q_error = 'q_error'
    lista = [inicial]
    myafd = Automata(simbolos,set(),dict(),inicial,set())
    #Breadth First Search
    while len(lista) != 0 :
        elem = lista[0]
        if not elem in myafd.getEstados():
            myafd.addEstado(elem)
            if afd.esFinal(elem):
                myafd.addFinales(elem)
            for i in simbolos:
                next_estado = afd.estadoSiguiente(elem,i)
                if next_estado == None:
                    myafd.addEstado(q_error)
                    myafd.addTransicion(elem,i,q_error)
                else:
                    myafd.addTransicion(elem,i,next_estado)
                    lista[len(lista):] = [next_estado]
        del lista[0]
    #Add q_error transitions
    if q_error in myafd.getEstados():
        for i in myafd.getSimbolos():
            myafd.addTransicion(q_error,i,q_error)
            
    return myafd   

    #Receives a final table from the Marked Triangular algorithm
    #Return an array with the equivalent states
def equivStates(T):
    #Equivalence tree
    equiv = [-1] * len(T)
    #Iterate over the table to find no marked elements
    for j in range(1, len(T), 1):
        i = 0
        while i < j:
            if not T[j][i][0]:
                equiv[j] = i
            i += 1
    count = 0        
    #Join equivalent states
    for n in range(len(equiv)):
        aux  = n
        if equiv[n]==-1: count += 1
        while equiv[aux] != -1:
            aux = equiv[aux]
        if n!=aux:
            equiv[n] = aux    
        
    return (equiv,count)


    #C:\Users\JoséManuel\Documents\GitHub\automatons-in-python\task1\in1.jffs
    #Receives a complete automata with no inaccessible states and
    #Return a pair with:
    # A dictionary that translates old states to new ones
    # A matrix 
def markTriangTable(myafd):
    #Entrada: un AFD M = (Q; V; delta; q0; F) con Q = {q0,...,qn}, V = {a1,...,ap}.
    #devuelve: un diccionario cuyas claves son los estados originales y sus valores son los estados minimos.
    #1. M <--- eliminaInaccesibles(M); //modifica M para que no tenga estados inaccesibles.
    #2. M <--- completaAFD(M); //modifica M para que sea un AFD completo.
    #3. Construye una tabla T con filas desde q1 (segundo estado) hasta qn (último) y columnas desde
        #q0 (primer estado) hasta qn-1 (penúltimo);
    alfabeto = myafd.getSimbolos() 
    estados = list(myafd.getEstados())
    n_estados = len(estados)
    indices = {}
    for i in range(n_estados):
        indices[estados[i]] = i
    finales = myafd.getFinales()

    #4. para cada casilla(qj; qi) de T hacer:
        #5. Asocia una lista(qj; qi) de parejas de estados //inicialmente vacía

    #Tabla de tamaño: n_estados x n_estados x (1+len(lista))
    T = [[[False,[]] for x in range(n_estados)] for y in range(n_estados)]

    #-----/* Marcado inicial de estados distinguibles */-----
    #6. para cada casilla(qj; qi) de T hacer:
        #7. si en la pareja (qj; qi) uno es final y el otro no entonces marcar(casilla(qj; qi));
    for i in finales:
        try:    
            index = estados.index(i)
            for n in range(n_estados):
                if n < index:
                    T[index][n][0] = True
                elif n > index:
                    T[n][index][0] = True
        except ValueError:
            print('Este automata no tienes estados finales', file= sys.stderr)

    #-----/* Deducción de estados distinguibles */------
    #8. para cada casilla(qj; qi) de T hacer: //ej., realizar recorrido por filas de la tabla
    for j in range(1, n_estados, 1):
        i = 0
        while i < j: 
            #9. si casilla(qj; qi) no marcada entonces
            if not T[j][i][0]:
                #10. para cada símbolo a_k del alfabeto hacer:
                for s in alfabeto:
                    #11. e1 := delta(qj; a_k); e2 := delta(qi; a_k); // obtiene pareja de estados leyendo a_k
                    estado1 = myafd.nextEstado(estados[i],s)
                    estado2 = myafd.nextEstado(estados[j],s) 
                    e1, e2 = indices[estado1], indices[estado2]
                    if e1 >= e2:
                        i1,i2 = e1,e2
                    else:
                        i1,i2 = e2,e1
                    #12. si casilla(e1; e2) está marcada entonces
                    if T[i1][i2][0]:
                        #13. marcarRecursivamente (casilla(qj; qi));
                        a_marcar = [tuple([j,i])]
                        while len(a_marcar) !=0 :
                            o = a_marcar[0]
                            T[o[0]][o[1]][0] = True
                            #Recorremos la lista de casillas asociadas
                            for k in range(0, len(T[o[0]][o[1]][1])):
                                par = T[o[0]][o[1]][1][k]
                                #Si no esta marcada la marcamos y la metemos a la lista 
                                if not T[par[0]][par[1]][0]:
                                    a_marcar.append(tuple([par[0],par[1]]))
                                    T[par[0]][par[1]][0] = True                    
                            del a_marcar[0]                   
                        #14. break; //no prueba con más símbolos, porque (qj; qi) son distinguibles
                        #// pasa a tratar la siguiente casilla
                        break
                    #15. si-no si (e1 != e2) y casilla(e1; e2) != casilla(qj; qi) entonces
                    elif i1!=i2 and (i1!=j or i2!=i):
                        #16. añade la pareja actual (qj; qi) a la lista de pareja obtenida: lista(e1; e2);
                        T[i1][i2][1].append(tuple([j,i]))
            i += 1
    #17. //fin de marcado de tabla triangular
    
    tabla_equivalencias = equivStates(T)
    lista_equiv = [[] for x in range(tabla_equivalencias[1])] 
    traductor= {}
    back = 0
    for n in range(len(tabla_equivalencias[0])):
        if tabla_equivalencias[0][n]!=-1:
            lista_equiv[tabla_equivalencias[0][n]].append(estados[n])
            traductor[estados[n]] = lista_equiv[tabla_equivalencias[0][n]]
            back += 1
        else: 
            lista_equiv[n-back].append(estados[n])  
            traductor[estados[n]] = lista_equiv[n-back]

    return (traductor, lista_equiv)


    #TODO Remove
def minimizeAFD(myafd):
    '''
    entrada: un autómata finito determinista M = (Q; V; delta; q0; F).
    devuelve: M_min = (Q_min; V; delta_min; q0_min; F_min) tal que
    M_min es mínimo y L(M_min) = L(M) (equivalente a M).
    -----/* Aplica el algoritmo de marcado de tabla triangular al autómataM. Este método
            previamente elimina estados inaccesibles y completa el autómata M */--------
    1. T <---- marcarTablaTriangular(M);
    
    -----/* Obtiene el conjunto de estados del autómata mínimo */------
    2. Obtener el conjunto cociente de Q/= a partir de la tabla T y hacer Q_min := Q/=;

    -----/* Obtiene el estado inicial del autómata mínimo: es el estado-clase S que contiene
            al estado inicial original */----------
    3. q0_min := S pertenece a Q_min tal que q0 pertenece a S;

    -----/* Obtiene el conjunto de estados finales del autómata mínimo */-----
    4. F_min := {S pertenece a Q_min | interserc(S, F) != null}; // estado-clase que contienen un final de M

    -----/* Obtiene la función de transición del autómata mínimo */------
    5. Para todo estado-clase S de Qmin y todo símbolo a de V hacer
        Se escoge un estado cualquiera q perteneciente a S;
        Se obtiene la transición:
        delta_min(S, a) := S' perteneciente a Q_min tal que delta(q; a) pertenece S';
    6. devuelve (Mmin)
    '''
    
    return# minimos
       
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
            print('El fichero no existe ',file=sys.stderr)
            ruta = input('Enter an input file:')
        except Exception as error:
            print('Problemas: ',error,file=sys.stderr)
            sys.exit(0)
    
    #Minimize the Automaton:
    myafd = myPerfectAFD(automata)
    estados_minimos = markTriangTable(myafd)
    traductor = estados_minimos[0]
    minimos = estados_minimos[1]
    simbols = list(myafd.getSimbolos())
    
    #Show the formatted answer
    table = [[] for x in range(len(minimos))] 
    for x in range(len(minimos)):
        if myafd.getInicial() in minimos[x]:
            table[x].append("->"+ repr(minimos[x]))
        else:
            token = True
            for elem in myafd.getFinales():
                if elem in minimos[x]:
                    table[x].append("#"+ repr(minimos[x]))
                    token = False
                    break 
            if token: table[x].append(repr(minimos[x]))
        
    for y in range(len(simbols)):
        for x in range(len(minimos)):
            table[x].append(repr(traductor[myafd.nextEstado(minimos[x][0], simbols[y])]))   
    headers = ["States"]
    headers[1:] = simbols[0:]
        
    print(tabulate(table,headers, tablefmt="psql"))    
    #TODO Remove
    #(6) For the formatted answer
        #https://pypi.org/project/tabulate/
    #print(tabulate(table, headers, tablefmt="psql"))
    
    
    
    

