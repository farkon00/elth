from .header import Header 


class Generator:
    def __init__(self, header=None, program_headers=None):
        if header is None:
            header = Header()
        if program_headers is None:
            program_headers = []

        self.instructions = []
        self.header = header
        self.program_headers = program_headers

    def add_inst(self, *inst):
        for i in inst:
            self.instructions.extend(i)

    def generate(self):
        buf = self.header.generate()
        for i in self.program_headers:
            buf.extend(i.generate())
        buf.extend(self.instructions)
        return buf