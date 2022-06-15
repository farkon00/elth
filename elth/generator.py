from .header import Header, ProgramHeader


class Generator:
    def __init__(self, header: Header = None, program_headers: ProgramHeader = None) -> None:
        if header is None:
            header = Header()
        if program_headers is None:
            program_headers = []

        self.instructions = []
        self.header = header
        self.program_headers = program_headers

    def auto_phead(self) -> None:
        """
        Automatically generates program header for the current state of generator
        Will reset all current program headers
        If any changes will be added to generator, header may become invalid 
        """
        self.program_headers = [
            ProgramHeader(
                p_flags = 5, # readable executable
                p_filesz = len(self.instructions) + ProgramHeader.SIZEOF + Header.SIZEOF,
                p_memsz = len(self.instructions) + ProgramHeader.SIZEOF + Header.SIZEOF,
                p_vaddr = 0x400000, p_paddr = 0x400000, p_align = 0x1000
            )
        ]

    def add_inst(self, *inst : list[list[int] | bytes]) -> None:
        for i in inst:
            self.instructions.extend(i)

    def generate(self) -> bytes:
        buf = self.header.generate()
        for i in self.program_headers:
            buf.extend(i.generate())
        buf.extend(self.instructions)
        return bytes(buf)