
import sys

class CPU:

    def __init__(self):

        self.fl = 0b00000000
        self.ie = 0b00000000
        self.ir = 0b00000000
        self.mar = 0b00000000
        self.mdr = 0b00000000
        self.pc = 0x0000
        self.reg = [0x0000] * 7 + [0x00f4]
        self.ram = [0b00000000] * 256 #65536
        self.tree = {
            0b10100000: self._add,
            0b10101000: self._and,
            0b01010000: self.call,
            0b10100111: self.cmp,
            0b01100110: self.dec,
#             'div': self.div,
            0b00000001: self.hlt,
            0b01100101: self.inc,
#             'self': self.int,
            0b00010011: self.iret,
            0b01010101: self.jeq,
#             'jge': self.jge,
#             'jgt': self.jgt,
#             'jle': self.jle,
#             'jlt': self.jlt,
            0b01010100: self.jmp,
            0b01010110: self.jne,
            0b10000011: self.ld,
            0b10000010: self.ldi,
            0b10100100: self.mod,
            0b10100010: self.mul,
            0b00000000: self.nop,
            0b01101001: self._not,
            0b10101010: self._or,
            0b01000110: self.pop,
            0b01001000: self.pra,
            0b01000111: self.prn,
            0b01000101: self.push,
            0b00010001: self.ret,
            0b10101100: self.shl,
            0b10101101: self.shr,
            0b10000100: self.st,
#             'sub': self.sub,
            0b10101011: self.xor
        }

    def load(self, prg):

        address = 0x0000

        with open(prg) as f:

            for line in f:

                string_val = line.split("#")[0].strip()

                if string_val == '':

                    continue

                byte = int(string_val, 2)
                self.ram[address] = byte
                address += 1

    def _add(self, reg_a, reg_b):

        self.reg[reg_a] += self.reg[reg_b]

    def _and(self, reg_a, reg_b):

        self.reg[reg_a] &= self.reg[reg_b]

    def call(self, reg_a, reg_b):

        self.reg[7] -= 0x0001
        self.ram[self.reg[7]] = self.pc + 0x0002
        self.pc = self.reg[reg_a]

    def cmp(self, reg_a, reg_b):

        if self.reg[reg_a] > self.reg[reg_b]:
            
            self.fl = 0b00000100
        
        elif self.reg[reg_a] < self.reg[reg_b]:
            
            self.fl = 0b00000010
        
        else:
            
            self.fl = 0b00000001
    
    def dec(self, reg_a, reg_b):
        
        self.reg[reg_a] -= 1

    def hlt(self, reg_a, reg_b):

        self.ir = 0b00000001
    
    def inc(self, reg_a, reg_b):
        
        self.reg[reg_a] += 1

    def iret(self, reg_a, reg_b):

        pass

    def jeq(self, reg_a, reg_b):

        if self.fl == 0b00000001:
            
            self.call(reg_a, None)

    def jmp(self, reg_a, reg_b):

        self.pc = self.reg[reg_a]

    def jne(self, reg_a, reg_b):

        if self.fl != 0b00000001:
            
            self.call(reg_a, None)
    
    def ld(self, reg_a, reg_b):
        
        self.reg[reg_a] = self.ram[reg_b]

    def ldi(self, reg_a, reg_b):

        self.reg[reg_a] = reg_b

    def mod(self, reg_a, reg_b):

        if self.reg[reg_b] == 0:

            print('div by 0')
            self.hlt(None, None)

        self.reg[reg_a] %= self.reg[reg_b]

    def mul(self, reg_a, reg_b):

            self.reg[reg_a] *= self.reg[reg_b]
    
    def nop(self, reg_a, reg_b):
        
        pass

    def _not(self, reg_a, reg_b):

        self.reg[reg_a] = ~self.reg[reg_a] & 0b11111111

    def _or(self, reg_a, reg_b):

        self.reg[reg_a] |= self.reg[reg_b]

    def pop(self, reg_a, reg_b):

        self.reg[reg_a] = self.ram[self.reg[7]]
        self.reg[7] += 0x0001
    
    def pra(self, reg_a, reg_b):
        
        print(chr(reg_a))

    def prn(self, reg_a, reg_b):

        print(self.reg[reg_a])

    def push(self, reg_a, reg_b):

        self.reg[7] -= 0x0001
        self.ram[self.reg[7]] = self.reg[reg_a]

    def ret(self, reg_a, reg_b):

        self.pc = self.ram[self.reg[7]]
        self.reg[7] += 0x0001

    def shl(self, reg_a, reg_b):

        self.reg[reg_a] <<= 1

    def shr(self, reg_a, reg_b):

        self.reg[reg_a] >>= 1

    def st(self, reg_a, reg_b):

        self.ram[reg_a] = reg_b

    def xor(self, reg_a, reg_b):

        self.reg[reg_a] ^= 1

    def run(self):

        self.pc = 0x0000
        self.ir = self.ram[self.pc]
#         i = 0

        while self.ir != 0b00000001:
            
#             i += 1
#             print()
#             print('op', i)
#             print('pc', hex(self.pc), 'ir', bin(self.ir))

            startpc = self.pc
            reg_a = self.ram[self.pc + 0x0001] if self.ram[self.pc] & 0b11000000 > 0b00000000 else None
            reg_b = self.ram[self.pc + 0x0002] if self.ram[self.pc] & 0b11000000 > 0b01000000 else None

            if self.ir in self.tree:

                self.tree[self.ir](reg_a, reg_b)

                if startpc == self.pc:

                    self.pc += int(reg_a != None) + int(reg_b != None) + 0x0001
    #                 self.pc += reg_a != None + reg_b != None + 0x0001

                self.ir = self.ram[self.pc]

            else:

                print("Unsupported operation")
                print('self.pc', hex(self.pc))
                print('self.ir', bin(self.ir))
                self.hlt(None, None)
