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
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = val
        self.pc += 2

    def pop(self, reg):
        val = self.ram[self.reg[self.SP]]
        self.reg[reg] = val
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
            if num_params == 2:
                self.branchtable[command](operand_a, operand_b)
            elif num_params == 1:
                self.branchtable[command](operand_a)
            else:
                running = self.branchtable[command]()
