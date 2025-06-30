class authDataError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class offerError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class accountError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class requestError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class connectionError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class floorsError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class giftsError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class tradingError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)