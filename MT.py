from rich import print

class MT:
    def __init__(self, states, initial_state, final_state, alphabet, tape_alphabet, function):
        self.states = states #Estados
        self.initial_state = initial_state #Estado inicial
        self.final_state = final_state #Estado final
        self.alphabet = alphabet #Alfabeto de entrada
        self.tape_alphabet = tape_alphabet #Alfabeto de la cinta
        self.function = function #Funcion de transicion

        # Tape Configuration
        self.headPosition = 0 #Posicion del cabezal actual
        self.tape = [] #La cinta que es la palabra de entrada
        self.currentState = initial_state #Estado actual

        self.error = ""

    def initializeTape(self, simulation_string): 
        # Cada vez que se quiera simular una palabra, se debe de llamar a esta funcion
        # Para que se reinicien las configuraciones de la cinta y el cabezal
        self.word = simulation_string
        self.tape = list(simulation_string)
        self.currentState = self.initial_state
        self.error = ""
        self.headPosition = 0

    def moveTape(self):
    
        # Se retorna true o false dependiendo si falla o no la maquina, por eso esta el
        # self.error porque asi se puede desplegar que paso

        # Si el primer movimiento es a la izquierda, entonces hay un error
        if self.headPosition < 0:
            self.tape.insert(0, "B")
            self.headPosition = 0
        
        # Si el cabezal esta fuera de la cinta, entonces se agrega un espacio en blanco
        if self.headPosition >= len(self.tape):
            self.tape.append("B")
        
        # Se obtiene el simbolo de la cinta en la posicion actual del cabezal
        currentTapeSymbol = self.tape[self.headPosition]

        # Si no hay una funcion definida para el estado actual y el simbolo de la cinta, entonces hay un error
        # function funciona por tuplas (estado, simbolo) asi que busca si existe una transicion
        if (self.currentState, currentTapeSymbol) not in self.function:
            self.error = "Error: No function defined for the current state and tape symbol"
            return False
        # Se obtiene la siguiente configuracion de la cinta y el estado
        nextState, nextTapeSymbol, tapeDisplacement = self.function[(self.currentState, currentTapeSymbol)]

        # Se actualiza el simbolo de la cinta en la posicion actual del cabezal
        self.tape[self.headPosition] = nextTapeSymbol

        # Se actualiza la posicion del cabezal dependiendo de la direccion
        if tapeDisplacement == "R":
            self.headPosition += 1
        elif tapeDisplacement == "L":
            self.headPosition -= 1
            if self.headPosition < 0:
                self.tape.insert(0, "B")
                self.headPosition = 0

        # Se actualiza el estado actual
        self.currentState = nextState
        return True
        

    def printCurrentTape(self):
        # Representa la cinta con el cabezal indicando la posición actual
        tape_with_head = ''.join(self.tape)
        tape_visual = (
            tape_with_head[:self.headPosition] + 
            "[" + tape_with_head[self.headPosition] + "]" + 
            tape_with_head[self.headPosition + 1:]
            if 0 <= self.headPosition < len(self.tape) 
            else "[B]"
        )
        
        # Imprime el estado actual, la cinta y la posición del cabezal
        print(f"[bold cyan]Estado actual[/bold cyan]: {self.currentState}")
        print(f"Cinta: {tape_visual}")
        print(f"Posición del cabezal: {self.headPosition}")


    #Simula la cadena
    def simulateMT(self):
        cont = 0
        while True:
            self.printCurrentTape()
            if self.currentState in self.final_state and self.currentState == "reject":
                return True, cont

            if self.currentState == self.final_state:
                result = ''.join([char for char in self.tape if char != 'B'])
                print(f"[green]Cinta final transformada: {result}[/green]")
                print("[green]Salida de la máquina: ", len(result))
                return True, cont
            cont += 1

            if not self.moveTape():
                return False, cont