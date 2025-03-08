from Reader import Reader
from MT import MT
import time 
reader = Reader("maquina.yml")



mt = MT(reader.states, reader.initial_state, reader.final_state, reader.alphabet, reader.tape_alphabet, reader.function)

# "|||"

mt.initializeTape("|||||")

start_time = time.time()
b, c = mt.simulateMT()
end_time = time.time()

print("Tiempo de ejecución: ", end_time - start_time) 
print("Cantidad de pasos: ", c) 