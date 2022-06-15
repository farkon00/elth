from dataclasses import dataclass


@dataclass
class EIdent:
    osabi: int = 0
    
    def generate(self):
        buf = [0x7F, 0x45, 0x4c, 0x46] # ELF magic
        buf.extend([2, 1, 1]) # EI_CLASS, EI_DATA, EI_VERSION. Library only works with this values
        buf.append(self.osabi)
        buf.extend([0] * 8)

        assert len(buf) == 16, "Wrong length of e_ident in header.EIdent.generate()"

        return buf


class Header:
    def __init__(self, 
     e_ident=None, e_type: int = 2, 
     e_machine: int = 3, e_version: int = 1,
     e_flags: int = 0):
        assert e_type < 65536, "e_type must fit in 16 bits"
        assert e_machine < 65536, "e_machine must fit in 16 bits"
        assert e_version < 4294967296, "e_version must fit in 32 bits"
        assert e_flags < 4294967296, "e_flags must fit in 32 bits"

        if e_ident is None:
            e_ident = EIdent()

        self.e_ident = e_ident
        self.e_type = e_type
        self.e_machine = e_machine
        self.e_version = e_version
        self.e_flags = e_flags
    
    def generate(self):
        buf = self.e_ident.generate()

        buf.extend([*self.e_type.to_bytes(2, "little"), *self.e_machine.to_bytes(2, "little"), 
                    *self.e_version.to_bytes(4, "little")])

        buf.extend([0] * 8) # e_entry
        buf.append(64) # value of e_phoff
        buf.extend([0] * 7) # padding of e_phoff
        buf.extend([0] * 8) # e_shoff

        buf.extend(self.e_flags.to_bytes(4, "little"))

        buf.extend([64, 0, 0x38, 0, 0x01, 0, 0x40, 0]) # e_ehsize, e_phentsize, e_phnum, e_shentsize
        buf.extend([0] * 4) # e_shnum, e_shstrndx

        return buf