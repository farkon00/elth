from .header import Header 


class Generator:
    def __init__(self, header=None):
        if header is None:
            header = Header()

        self.header = header

    def generate(self):
        return self.header.generate()