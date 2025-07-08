class MachineKeyAlreadyExists(Exception):
    def __init__(self, message="A chave da máquina já existe.", key=None):
        self.key = key
        super().__init__(message)