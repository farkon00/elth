class Reg:
    RAX = 0xc0
    RBX = 0xc3
    RCX = 0xc1
    RDX = 0xc2
    RSI = 0xc6
    RDI = 0xc7
    RBP = 0xc5
    RSP = 0xc4
    R8  = 0xc8
    R9  = 0xc9
    R10 = 0xca
    R11 = 0xcb
    R12 = 0xcc
    R13 = 0xcd
    R14 = 0xce
    R15 = 0xcf


def mov(reg: int | str, value: int):
    if isinstance(reg, str):
        reg = getattr(Reg, reg)
    if 207 >= reg >= 192:
        return [0x48, 0xc7, reg, *value.to_bytes(4, "little")]
    else:
        raise ValueError("Invalid register(only 64-bit one supported currently)")