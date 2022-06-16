from dataclasses import dataclass


@dataclass
class EIdent:
    osabi: int = 3
    
    def generate(self):
        buf = [0x7F, 0x45, 0x4c, 0x46] # ELF magic
        buf.extend([2, 1, 1]) # EI_CLASS, EI_DATA, EI_VERSION. Library only works with this values
        buf.append(self.osabi)
        buf.extend([0] * 8)

        assert len(buf) == 16, "Wrong length of e_ident in header.EIdent.generate()"

        return buf

class EType:
    NONE = 0x00
    REL = 0x01
    EXEC = 0x02
    DYN = 0x03
    CORE = 0x04
    LOOS = 0xFE00
    HIO = 0xFEFF
    LOPROC = 0xFF00
    HIPRO = 0xFFFF

class PType:
    NULL = 0x00000000
    LOAD = 0x00000001
    DYNAMIC = 0x00000002
    INTERP = 0x00000003
    NOTE = 0x00000004
    SHLIB = 0x00000005
    PHDR = 0x00000006
    TLS = 0x00000007
    LOOS = 0x60000000
    HIO = 0x6FFFFFFF
    LOPROC = 0x70000000
    HIPRO = 0x7FFFFFFF

class ProgramHeader:
    SIZEOF = 0x38

    def __init__(self,
     p_type=PType.LOAD, p_flags=0, 
     p_offset=0, p_vaddr=0, p_paddr=0,
     p_filesz=0, p_memsz=0):
        assert p_type < 4294967296, "p_type must fit in 32 bits"
        assert p_flags < 4294967296, "p_flags must fit in 32 bits"
        assert p_offset < 18446744073709551615, "p_offset must fit in 64 bits"
        assert p_vaddr < 18446744073709551615, "p_vaddr must fit in 64 bits"
        assert p_paddr < 18446744073709551615, "p_paddr must fit in 64 bits"
        assert p_filesz < 18446744073709551615, "p_filesz must fit in 64 bits"
        assert p_memsz < 18446744073709551615, "p_memsz must fit in 64 bits"

        self.p_type = p_type
        self.p_flags = p_flags
        self.p_offset = p_offset
        self.p_vaddr = p_vaddr
        self.p_paddr = p_paddr
        self.p_filesz = p_filesz
        self.p_memsz = p_memsz

    def generate(self):
        return [
            *self.p_type.to_bytes(4, byteorder="little"), *self.p_flags.to_bytes(4, byteorder="little"),
            *self.p_offset.to_bytes(8, byteorder="little"), *self.p_vaddr.to_bytes(8, byteorder="little"),
            *self.p_paddr.to_bytes(8, byteorder="little"), *self.p_filesz.to_bytes(8, byteorder="little"),
            *self.p_memsz.to_bytes(8, byteorder="little"), *0x1000.to_bytes(8, byteorder="little") # last one is p_align
        ]

class Header:
    SIZEOF = 0x40

    def __init__(self, 
     e_ident=None, e_type: int = EType.EXEC, 
     e_machine: int = 0x3e, e_version: int = 1,
     e_entry: int = 4194424, e_flags: int = 0,
     e_phnum: int = 1):
        assert e_type < 65536, "e_type must fit in 16 bits"
        assert e_machine < 65536, "e_machine must fit in 16 bits"
        assert e_version < 4294967296, "e_version must fit in 32 bits"
        assert e_flags < 4294967296, "e_flags must fit in 32 bits"
        assert e_phnum < 65536, "e_phnum must fit in 16 bits"

        if e_ident is None:
            e_ident = EIdent()

        self.e_ident = e_ident
        self.e_type = e_type
        self.e_machine = e_machine
        self.e_version = e_version
        self.e_entry = e_entry
        self.e_flags = e_flags
        self.e_phnum = e_phnum
    
    def generate(self):
        buf = self.e_ident.generate()

        buf.extend([*self.e_type.to_bytes(2, "little"), *self.e_machine.to_bytes(2, "little"), 
                    *self.e_version.to_bytes(4, "little"), *self.e_entry.to_bytes(8, "little")])

        buf.append(64) # value of e_phoff
        buf.extend([0] * 7) # padding of e_phoff
        buf.extend([0] * 8) # e_shoff

        buf.extend(self.e_flags.to_bytes(4, "little"))

        buf.extend([64, 0, *ProgramHeader.SIZEOF.to_bytes(2, "little")]) # e_ehsize, e_phentsize
        buf.extend(self.e_phnum.to_bytes(2, "little"))
        buf.extend([0x40, 0, *([0] * 4)]) # e_shentsize, e_shnum, e_shstrndx

        return buf