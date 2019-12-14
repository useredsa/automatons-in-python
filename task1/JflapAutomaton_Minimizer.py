#!/usr/bin/python3
import sys
from collections import deque
from jflap.Afd import Afd
from jflap.Transiciones import Transiciones
from tabulate import tabulate
 
 
class Automaton:
    """Wrapper for the class Afd. Allows easy operation
    over the automata by erasing unreachable states and
    adding an error state in case there it is not complete.
    """
    ERROR_STATE = "q_error"
    def __init__(self, afd):
        """Receives any automata and returns a complete automata
        without inaccessible states.
        """
        self.wrapped = afd
        self.states = []

        initial = afd.getEstadoInicial()
        if not initial:
            raise ValueError("The automata doesn't have an initial state")
        # Breadth First Search
        notComplete = False
        bfs = deque([initial])
        while bfs:
            state = bfs.popleft()
            if not state in self.states:
                self.states.append(state)
                for symb in self.getSymbols():
                    nextState = afd.estadoSiguiente(state, symb)
                    if not nextState:
                        notComplete = True
                    elif not nextState in self.states:
                        bfs.append(nextState)
        #Add q_error transitions
        if notComplete:
            self.states.append(self.ERROR_STATE)
        
    
    def getSymbols(self):
        return self.wrapped.getAlfabeto()
    def getStates(self):
        return self.states
    def getInitial(self):
        return self.wrapped.getEstadoInicial()
    def isFinal(self, state):
        return self.wrapped.esFinal(state)
    def nextState(self, state, symbol):
        nextState = self.wrapped.estadoSiguiente(state, symbol)
        return nextState or self.ERROR_STATE
   

    def equivStates(self, T):
        """Receives a final table from the Marked Triangular algorithm
        and returns a list where each element is a list of equivalent
        states and a lookup table where you can find the index of the
        equivalent state for each old state.
        """
        belongsTo = {}
        newStates = []
        numNewStates = 0

        for state in self.states:
            if state in belongsTo:
                continue
            belongsTo[state] = numNewStates
            newStates.append([state])
            for otherState in self.states:
                stateI = max(state, otherState)
                stateJ = min(state, otherState)
                if stateI != stateJ and not T[stateI, stateJ]:
                    belongsTo[otherState] = numNewStates
                    newStates[-1].append(otherState)
            numNewStates += 1
        
        return newStates, belongsTo


    def markDependencies(self, table, dependentPairs, stateI, stateJ):
        """Method used by triangularTable to mark states when it is
        found that they are different.
        """
        toMark = deque([stateI, stateJ])
        while toMark:
            stateA = toMark.popleft()
            stateB = toMark.popleft()
            table[stateA, stateB] = True
            # Insert in the queue the dependent pairs
            for otherPair in dependentPairs[stateA, stateB]:
                if not table[otherPair[0], otherPair[1]]:
                    table[otherPair[0], otherPair[1]] = True                                          
                    toMark.extend(otherPair)


    def triangularTable(self):
        """Receives a complete automata with no inaccessible states and
        returns a triangular table containing which states aren't equivalent.
        To query if the pair i,j is different, use table[max(i,j)][min(i,j)].
        """

        table = {}
        dependentPairs = {}
        # If a pair of states contains a final state and a non-final state,
        # then they are distinguishable.             
        for stateI in self.states:
            for stateJ in self.states:
                if stateI > stateJ:
                    table[stateI, stateJ] = self.isFinal(stateI) ^ self.isFinal(stateJ)
                    dependentPairs[stateI, stateJ] = []
                
            
        # Fill the table of distinguishable states
        for stateI in self.states: 
            for stateJ in self.states:
                # If both states were already marked as different
                if stateI <= stateJ or table[stateI, stateJ]:
                    continue
                # If both states lead with the same symbol to different states,
                # they must be distinguishable.
                for simb in self.getSymbols():
                    nextI = self.nextState(stateI,simb)
                    nextJ = self.nextState(stateJ,simb)
                    # Always consider pairs with the smaller name after!
                    # (to access the table)
                    if nextI <= nextJ:
                        nextI, nextJ = nextJ, nextI
                    if nextI == nextJ:
                        continue
                    if table[nextI, nextJ]:
                        # If our states are distinguisable, all that depended on this
                        # pair are also
                        self.markDependencies(table, dependentPairs, stateI, stateJ)
                        break
                    elif nextI != stateI or nextJ != stateJ:
                        # If we don't know yet whether the next 2 states are different,
                        # mark that if we find that they're different, we need to mark
                        # this one too.
                        dependentPairs[nextI, nextJ].append([stateI, stateJ])

        return table

    def printMinimizedAutomaton(self):
        """Receive a complete automata without inaccessible states
        and write to the console the representation of the minimize automata
        """
        #TODO remove
        print()
        # Logic of minimization
        # Create the triangular table of equivalent states
        triangT = self.triangularTable()
        # Merge equal states
        newStates, belongsTo = self.equivStates(triangT)
        
        # Create a table for printing
        table = []
        for newState in newStates:
            # Each row should contain
            # The state's name with identifier '->' if it's the initial
            # state and identifier '#' if it's a final state.
            identifier = '->' if self.getInitial() in newState else ''
            for state in newState:
                if self.wrapped.esFinal(state):
                    identifier += '#'
                    break
            # First column is this state's name
            table.append([identifier + repr(newState)])
            # The following columns contain transitions for each symbol
            for symb in self.getSymbols():
                nextOldState = self.nextState(newState[0], symb)
                nextNewState = newStates[belongsTo[nextOldState]]
                table[-1].append(repr(nextNewState))
        
        headers = ['States']
        headers[1:] = self.getSymbols()
        print(tabulate(table, headers, tablefmt='psql'))
       
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
    
    wrapper = Automaton(automata)
    wrapper.printMinimizedAutomaton()

