class HTTP404Error(Exception):
    def __init__(self, message="HTTP 404 - Not Found"):
        self.message = message
        super().__init__(self.message)