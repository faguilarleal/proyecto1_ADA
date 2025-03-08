from Reader import Reader
from MT import MT
from analisis import Analisis
reader = Reader("maquina.yml")



mt = MT(reader.states, reader.initial_state, reader.final_state, reader.alphabet, reader.tape_alphabet, reader.function)

# "|||"

mt.initializeTape("|||||||||")
mt.simulateMT()
Analisis()
