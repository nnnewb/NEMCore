class NetEaseError(Exception):
    def __init__(self, code, message=None, data=None, url=None, method=None):
        super().__init__(self, message)
        self.code = code
        self.message = message
        self.data = data
        self.url = None
        self.method = None

    def __str__(self):
        return self.message or self.__repr__()

    def __repr__(self):
        if self.method and self.url:
            return f'<NetEaseError {self.method} "{self.url}" {self.code} {self.message}>'
        else:
            return '<NetEaseError {} {}>'.format(self.code, self.message)
