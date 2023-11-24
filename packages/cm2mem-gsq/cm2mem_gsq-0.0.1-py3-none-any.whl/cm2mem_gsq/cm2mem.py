from string import ascii_lowercase, ascii_uppercase, digits

def pbin(num, width=4):
    if isinstance(num,str):
        num = int(num)
    binary_str = bin(num)[2:]
    padded_str = binary_str.zfill(width)
    return padded_str

class Memory:
    raw = []
    massive = True
    def __init__(self,massive=True) -> None:
        """Create an Memory instance. Will assume you're using a massivememory if massive is True."""
        for i in range(4096):
            self.raw.append(0)
        return
    def pack(self) -> str: 
        """Pack your code into a string to be pasted into a massivememory"""
        if self.massive:
            alphabet = ascii_uppercase + ascii_lowercase + digits + "+/"

            #35,168 = 0x8960
            instructions = ""
            for i in self.raw:
                hx = hex(i)[2:]
                instructions += ("0"*(4-len(hx))) + hx + " "
            instructions = instructions[:-1]
            instruction_bytes = bytes.fromhex(instructions)

            output = ""
            for b1, b2 in zip(instruction_bytes[::2], instruction_bytes[1::2]):
                bits = b1 << 8 | b2
                for _ in range(3):
                    output += alphabet[bits & 0x3f]
                    bits >>= 6

            return output + ("A" * (12288-len(output)))
        else:
            rawout = ""
            for i in self.raw:
                hx = hex(i)[2:]
                rawout += ("0"*(2-len(hx))) + hx + " "
            return rawout
    def __getitem__(self, key):
        if isinstance(key,str):
            key = int(key,2)
        return self.raw[key]
    def __setitem__(self, key, value):
        if isinstance(key,str):
            key = int(key,2)
        if isinstance(value,str):
            value = int(value,2)
        self.raw[key] = value

class premade:
    """Functions to load pre-made 'programs' to a Memory instance, allowing you to do subtraction, addition, etc.. using a massivememory"""
    def divider(mem_instance : Memory) -> None:
        """6-bit divider (0 / 0 = 0). Outputs are rounded."""
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            if param2 == 0:
                fp[i] = 0
            else:
                fp[i] = int(round(param1/param2))

    def multiplier(mem_instance : Memory) -> None:
        """6-bit multiplier"""
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            fp[i] = param1*param2

    def adder(mem_instance : Memory) -> None:
        """6-bit adder"""
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            fp[i] = param1+param2
        
    def subtractor(mem_instance : Memory) -> None:
        """6-bit subtractor (any result below 0 just outputs 0)"""
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            if param1-param2 < 0:
                fp[i] = 0
            else:
                fp[i] = param1-param2

    def displaydriver(mem_instance : Memory) -> None:
        """For a 4 digit seven segment display (displays the number fed into the input)"""
        fp = mem_instance
        for i in range(4096):
            st = ('0' * (4-len(str(i)))) + str(i)
            fp[i] = pbin(st[3]) + pbin(st[2]) + pbin(st[1]) + pbin(st[0])