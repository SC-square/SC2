class Opcode:
    '''
    public class
    '''
    SIZE = 1  # all opcodes are 1-byte

    def __init__(self, opcode: int, name: str, operandSize: int, stackPopSize: int, stackPushSize: int, gas: int, description: str) -> None:
        self.opcode = opcode
        self.name = name
        self.operandSize = operandSize
        self.stackPopSize = stackPopSize
        self.stackPushSize = stackPushSize
        self.gas = gas
        self.description = description

    def __str__(self) -> str:
        # e.g. (0x60) PUSH1
        return f"(0x{self.opcode:02x}) {self.name}"
