class NetEaseError(Exception):
    def __init__(self, code, message=None, data=None):
        super().__init__(self, message)
        self.code = code
        self.message = message
        self.data = data

    def __repr__(self):
        return '<NetEaseError {} {}>'.format(self.code, self.message)
