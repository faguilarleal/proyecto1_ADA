import yaml

class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

        self.states = []
        self.initial_state = ""
        self.final_state = ""
        self.reject_state = ""

        self.alphabet = []
        self.tape_alphabet = []
        self.simulation_strings = []
        self.function = {}
        self.machine_type = ""
        
        self.readFile()
        self.parseData(self.data)


    def readFile(self):
        with open(self.file_path, 'r') as file:
            self.data = yaml.safe_load(file)

    def parseData(self, data):
        states = data["q_states"]

        self.states = states["q_list"]
        self.initial_state = states["initial"]
        self.final_state = states["final"]

        self.alphabet = data["alphabet"]
        self.tape_alphabet = data["tape_alphabet"]

        # self.simulation_strings = data["simulation_strings"]
        tempFunction = data["delta"]
        for transition in tempFunction:
            self.function[(transition["params"]["initial_state"], transition["params"]["tape_input"])] = (transition["output"]["final_state"], transition["output"]["tape_output"], transition["output"]["tape_displacement"])


    def printData(self):
        print(f"Tipo de maquina: {self.machine_type}")
        print(self.states)
        print(self.initial_state)
        print(self.final_state)
        print(self.alphabet)
        print(self.tape_alphabet)
        print(self.simulation_strings)
        print(self.function)