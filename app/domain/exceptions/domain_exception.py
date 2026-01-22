class DomainException(Exception):
    code: str
    message: str
    status: int

    def __init__(self, code, message, status):
        self.code = code
        self.message = message
        self.status = status
        super().__init__(self.message)