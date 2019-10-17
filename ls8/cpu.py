"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.SP = 7
        self.commands = {
            'LDI': int("10000010", 2),
            'PRN': int("01000111", 2),
            'HLT': int("00000001", 2),
            'MUL': int("10100010", 2),
            'PUSH': int("01000101", 2),
            'POP': int("01000110", 2),
        }
        self.branchtable = {
            self.commands['LDI']: self.ldi,
            self.commands['PRN']: self.prn,
            self.commands['HLT']: self.hlt,
            self.commands['MUL']: self.mul,
            self.commands['PUSH']: self.push,
            self.commands['POP']: self.pop,
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
        # elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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

    def ldi(self, reg_a, value):
        self.reg[reg_a] = value
        self.pc += 3

    def prn(self, reg_a):
        print(f'Value: {self.reg[reg_a]}')
        self.pc += 2

    def mul(self, reg_a, reg_b):
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def hlt(self):
        self.pc += 1
        print('Stopping...')
        return False

    def push(self, reg):
        val = self.reg[reg]
        # Decrement the SP.
        self.reg[self.SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        self.ram[self.reg[self.SP]] = val
        self.pc += 2

    def pop(self, reg):
        val = self.ram[self.reg[self.SP]]
        # Copy the value from the address pointed to by SP to the given register.
        self.reg[reg] = val
        # Increment SP.
        self.reg[self.SP] += 1
        self.pc += 2

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            command = self.ram[self.pc]
            num_params = int(bin(command >> 6).replace("0b", ""), 2)
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            # print(f'command: {command}, operand_a: {operand_a}, operand_b: {operand_b}')
            if num_params == 2:
                self.branchtable[command](operand_a, operand_b)
            elif num_params == 1:
                self.branchtable[command](operand_a)
            else:
                running = self.branchtable[command]()
            # if command == self.commands['LDI']:  # set register (operand_a) to value (operand_b)
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # elif command == self.commands['PRN']:  # print value of register (operand_a)
            #     print(f'Value: {self.reg[operand_a]}')
            #     self.pc += 2
            # elif command == self.commands[
            #     'MUL']:  # multiply value of two registers (operand_a and operand_b) and stores in operand_a
            #     # self.reg[operand_a] *= self.reg[operand_b]
            #     self.alu('MUL', operand_a, operand_b)
            #     self.pc += 3
            # elif command == self.commands['HLT']:  # stops running
            #     running = False
            #     self.pc += 1
            #     print('Stopping...')
            # else:
            #     running = False
            #     print(f'Unknown command: {command}')
