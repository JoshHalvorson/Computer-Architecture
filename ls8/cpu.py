"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.commands = {
            'LDI': int("10000010", 2),
            'PRN': int("01000111", 2),
            'HLT': int("00000001", 2)
        }

    def load(self, filename):
        """Load a program into memory."""
        # address = 0
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#")
                    # Convert any numbers from binary strings to integers
                    num = comment_split[0].strip()
                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue
                    self.ram[address] = val
                    address += 1
                    # print(f"{val:08b}: {val:d}")
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        # return value stored in passed in address
        return self.ram[address]

    def ram_write(self, value, address):
        # writes the given value into given address
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            command = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            if command == self.commands['LDI']:  # set register (operand_a) to value (operand_b)
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == self.commands['PRN']:  # print value of register (operand_a)
                print(f'Value: {self.reg[operand_a]}')
                self.pc += 2
            elif command == self.commands['HLT']:  # stops running
                running = False
                self.pc += 1
                print('Stopping...')
            else:
                running = False
                print(f'Unknown command: {command}')